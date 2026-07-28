from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from main import ctx

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse("home.html", ctx(request))
