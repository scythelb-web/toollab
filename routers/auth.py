from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import os

router = APIRouter()

# Simple in-memory user store (replace with DB for production)
# For now: email-based "accounts" stored in session

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "login.html", {"request": request, "subdomain": request.state.subdomain,
                        "user": request.session.get("user")}
    )

@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Simple session-based auth for MVP
    request.session["user"] = {"email": email}
    request.session["openai_key"] = request.session.get("openai_key", "")
    return RedirectResponse("/", status_code=303)

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "signup.html", {"request": request, "subdomain": request.state.subdomain,
                         "user": request.session.get("user")}
    )

@router.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...)):
    request.session["user"] = {"email": email}
    return RedirectResponse("/", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@router.get("/account", response_class=HTMLResponse)
async def account(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/auth/login", status_code=303)
    return request.app.state.templates.TemplateResponse(
        "account.html", {"request": request, "user": user, "subdomain": request.state.subdomain}
    )

@router.post("/settings")
async def save_settings(request: Request, openai_key: str = Form("")):
    request.session["openai_key"] = openai_key
    return RedirectResponse("/auth/account", status_code=303)
