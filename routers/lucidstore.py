"""
LucidStore — Signs & Stickers (separate from ToolLab subscription).
Contact: lucidify@gmail.com
Inquiries are emailed via SendGrid with clear ToolLab attribution.
"""

import os
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from context import ctx

router = APIRouter()

STORE_EMAIL = "lucidify@gmail.com"
STORE_NAME = "LucidStore"
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDER_EMAIL = "scythelb@gmail.com"


def _send_inquiry_email(inquiry: dict) -> bool:
    """Send inquiry to lucidify@gmail.com via SendGrid API.
    Email clearly shows it came via ToolLab — Scy's referral."""
    if not SENDGRID_API_KEY:
        return False

    body_html = f"""<h2>New LucidStore Inquiry via ToolLab</h2>
<p><strong>This lead came from Scy's site — ToolLab referral.</strong></p>
<hr>
<table>
  <tr><td><strong>Name:</strong></td><td>{inquiry['name']}</td></tr>
  <tr><td><strong>Email:</strong></td><td>{inquiry['email']}</td></tr>
  <tr><td><strong>Service:</strong></td><td>{inquiry['service']}</td></tr>
</table>
<hr>
<h3>Project Details</h3>
<p>{inquiry['message']}</p>
<p style="color:#888;font-size:12px;margin-top:24px">
  Sent via ToolLab LucidStore inquiry form · toollab.ca/lucidstore
</p>"""

    payload = {
        "from": {"email": SENDER_EMAIL, "name": "ToolLab LucidStore"},
        "subject": f"New LucidStore inquiry from ToolLab — {inquiry['name']}",
        "personalizations": [{"to": [{"email": STORE_EMAIL, "name": "LucidStore"}]}],
        "content": [{"type": "text/html", "value": body_html}],
    }

    try:
        resp = httpx.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=15,
        )
        return resp.is_success
    except Exception:
        return False


@router.get("/", response_class=HTMLResponse)
async def lucidstore_home(request: Request):
    return request.app.state.templates.TemplateResponse(
        "lucidstore.html",
        ctx(request, store_email=STORE_EMAIL, store_name=STORE_NAME),
    )


@router.post("/", response_class=HTMLResponse)
async def lucidstore_inquire(
    request: Request,
    name: str = Form(""),
    email: str = Form(""),
    message: str = Form(""),
    service: str = Form("Signs"),
):
    inquiry = {
        "name": name,
        "email": email,
        "service": service,
        "message": message,
    }

    email_sent = _send_inquiry_email(inquiry)

    return request.app.state.templates.TemplateResponse(
        "lucidstore.html",
        ctx(
            request,
            store_email=STORE_EMAIL,
            store_name=STORE_NAME,
            submitted=True,
            email_sent=email_sent,
            inquiry=inquiry,
        ),
    )
