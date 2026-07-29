"""
toollab.ca — AI-powered utility tools hub
Subdomain routing: pdf.* / image.* / voice.* / www.*
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers import home, pdf, image, voice, auth, stripe, qr, text, calc, sitemap
from context import ctx

app = FastAPI(title="ToolLab", version="1.0.0")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "dev-secret-change-me"))
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")
app.state.templates = templates

# --- Subdomain detection middleware ---
@app.middleware("http")
async def detect_subdomain(request: Request, call_next):
    host = request.headers.get("host", "")
    subdomain = host.split(".")[0].lower() if "." in host else "www"
    valid = {"pdf", "image", "voice", "www"}
    request.state.subdomain = subdomain if subdomain in valid else "www"
    request.state.tool_name = {
        "pdf": "PDF Tools", "image": "Image Tools",
        "voice": "Voice Tools", "www": "ToolLab"
    }.get(request.state.subdomain, "ToolLab")
    return await call_next(request)

# --- Routers ---
app.include_router(home.router)
app.include_router(pdf.router, prefix="/pdf")
app.include_router(image.router, prefix="/image")
app.include_router(voice.router, prefix="/voice")
app.include_router(auth.router, prefix="/auth")
app.include_router(stripe.router, prefix="/stripe")
app.include_router(qr.router, prefix="/qr")
app.include_router(text.router, prefix="/text")
app.include_router(calc.router, prefix="/calc")
app.include_router(sitemap.router)  # root-level for /sitemap.xml

# Pricing page
@app.get("/pricing")
async def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", ctx(request))

# Health check
@app.get("/health")
async def health():
    return {"service": "ToolLab", "status": "ok"}

# Google AdSense verification
@app.get("/ads.txt")
async def ads_txt():
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(
        "google.com, pub-8191097225084387, DIRECT, f08c47fec0942fa0",
        media_type="text/plain"
    )
