from fastapi import APIRouter, Request, File, Form, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from PIL import Image
import io

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def image_home(request: Request):
    return request.app.state.templates.TemplateResponse(
        "tool_image.html", {"request": request, "subdomain": request.state.subdomain,
                             "user": request.session.get("user")}
    )

@router.post("/remove-bg")
async def remove_background(request: Request, file: UploadFile = File(...)):
    from rembg import remove
    img = await file.read()
    result = remove(img)
    return StreamingResponse(io.BytesIO(result), media_type="image/png",
                             headers={"Content-Disposition": f"attachment; filename=nobg_{file.filename}.png"})

@router.post("/upscale")
async def upscale_image(request: Request, file: UploadFile = File(...), scale: int = Form(2)):
    img = Image.open(io.BytesIO(await file.read()))
    w, h = img.size
    img = img.resize((w * scale, h * scale), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png",
                             headers={"Content-Disposition": f"attachment; filename=upscaled_{file.filename}.png"})

@router.get("/palette", response_class=HTMLResponse)
async def palette_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "tool_image.html", {"request": request, "subdomain": request.state.subdomain,
                             "active_tab": "palette", "user": request.session.get("user")}
    )
