"""
LucidStore — Signs & Stickers (separate from ToolLab subscription).
Contact: lucidify@gmail.com
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from context import ctx

router = APIRouter()

STORE_EMAIL = "lucidify@gmail.com"
STORE_NAME = "LucidStore"


@router.get("/", response_class=HTMLResponse)
async def lucidstore_home(request: Request):
    return request.app.state.templates.TemplateResponse(
        "lucidstore.html",
        ctx(request, store_email=STORE_EMAIL, store_name=STORE_NAME),
    )


@router.post("/")
async def lucidstore_inquire(
    request: Request,
    name: str = Form(""),
    email: str = Form(""),
    message: str = Form(""),
    service: str = Form("Signs"),
):
    """Handle inquiry form submission — displays confirmation (email sending is
    placeholder until SMTP is configured)."""
    return request.app.state.templates.TemplateResponse(
        "lucidstore.html",
        ctx(
            request,
            store_email=STORE_EMAIL,
            store_name=STORE_NAME,
            submitted=True,
            inquiry={
                "name": name,
                "email": email,
                "service": service,
                "message": message,
            },
        ),
    )
