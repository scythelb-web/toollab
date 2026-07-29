"""Text tools router — serves the text tools page."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from context import ctx

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def text_home(request: Request):
    return request.app.state.templates.TemplateResponse("tool_text.html", ctx(request))
