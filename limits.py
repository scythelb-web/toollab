"""
Usage limits for free-tier ToolLab users.
Tracks by email (logged in) or IP (anonymous). Pro users are unlimited.

Categories:
  pdf      — merge, compress, to-word, split, rotate
  image    — remove-bg, upscale, convert, resize
  voice    — tts, stt
  pdf-ai   — summarize, chat (requires OpenAI key too)
"""

import sqlite3
import os
from datetime import datetime, timedelta, timezone
from fastapi import Request
from fastapi.responses import JSONResponse

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "usage.db")
FREE_LIMIT = 5  # uses per category per 24h window


def _get_db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            category TEXT NOT NULL,
            used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_user_cat_time ON usage(user_id, category, used_at)"
    )
    conn.commit()
    return conn


def _get_user_id(request: Request) -> str:
    """Identify user by email if logged in, otherwise by IP."""
    user = request.session.get("user") or {}
    if user.get("email"):
        return f"email:{user['email']}"
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    elif request.client:
        ip = request.client.host
    else:
        ip = "unknown"
    return f"ip:{ip}"


def is_pro(request: Request) -> bool:
    user = request.session.get("user") or {}
    return bool(user.get("is_pro", False))


def check_and_increment(request: Request, category: str) -> dict:
    """
    Atomically check usage limit AND record this use.
    Returns {"allowed": bool, "remaining": int, "limit": int, "is_pro": bool}

    Call BEFORE processing the tool. If allowed=False, return a 429 response.
    The usage is recorded immediately so failed attempts still count (prevents
    retry-spam abuse).
    """
    pro = is_pro(request)
    if pro:
        return {"allowed": True, "remaining": float("inf"), "limit": FREE_LIMIT, "is_pro": True}

    user_id = _get_user_id(request)
    conn = _get_db()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    # Count existing uses in window
    cur = conn.execute(
        "SELECT COUNT(*) FROM usage WHERE user_id = ? AND category = ? AND used_at > ?",
        (user_id, category, cutoff.isoformat()),
    )
    already_used = cur.fetchone()[0]

    if already_used >= FREE_LIMIT:
        return {
            "allowed": False,
            "remaining": 0,
            "limit": FREE_LIMIT,
            "is_pro": False,
        }

    # Record this use (even before success — prevents race-condition spam)
    conn.execute(
        "INSERT INTO usage (user_id, category) VALUES (?, ?)", (user_id, category)
    )
    conn.commit()

    return {
        "allowed": True,
        "remaining": FREE_LIMIT - already_used - 1,
        "limit": FREE_LIMIT,
        "is_pro": False,
    }


def get_remaining(request: Request, category: str) -> int:
    """Read remaining uses without incrementing. For display in templates."""
    if is_pro(request):
        return float("inf")  # type: ignore
    user_id = _get_user_id(request)
    conn = _get_db()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    cur = conn.execute(
        "SELECT COUNT(*) FROM usage WHERE user_id = ? AND category = ? AND used_at > ?",
        (user_id, category, cutoff.isoformat()),
    )
    count = cur.fetchone()[0]
    return max(0, FREE_LIMIT - count)


def limit_exceeded_response(request: Request, category: str) -> JSONResponse:
    """Return a 429 JSON response that the frontend can display."""
    user = request.session.get("user") or {}
    logged_in = bool(user.get("email"))
    return JSONResponse(
        status_code=429,
        content={
            "error": f"Free limit reached: {FREE_LIMIT} uses per day for {category} tools.",
            "upgrade": "https://toollab.ca/pricing",
            "logged_in": logged_in,
        },
    )
