"""Calculator tools router."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from context import ctx

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def calc_home(request: Request):
    return request.app.state.templates.TemplateResponse("tool_calc.html", ctx(request))
