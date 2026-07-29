from fastapi import APIRouter, Request, File, Form, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from PIL import Image
import io
from context import ctx

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def image_home(request: Request):
    return request.app.state.templates.TemplateResponse("tool_image.html", ctx(request))

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

@router.post("/convert")
async def convert_image(request: Request, file: UploadFile = File(...), fmt: str = Form("png")):
    """Convert image to PNG, JPEG, or WebP."""
    img = Image.open(io.BytesIO(await file.read()))
    if img.mode in ("RGBA", "P") and fmt.lower() == "jpeg":
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format=fmt.upper())
    buf.seek(0)
    name = file.filename.rsplit(".", 1)[0] if file.filename else "converted"
    return StreamingResponse(buf, media_type=f"image/{fmt.lower()}",
                             headers={"Content-Disposition": f"attachment; filename={name}.{fmt.lower()}"})

@router.post("/resize")
async def resize_image(request: Request, file: UploadFile = File(...),
                        width: int = Form(0), height: int = Form(0), percent: int = Form(0)):
    """Resize image by dimensions or percentage."""
    img = Image.open(io.BytesIO(await file.read()))
    w, h = img.size
    if percent > 0:
        w, h = int(w * percent / 100), int(h * percent / 100)
    elif width > 0 and height > 0:
        w, h = width, height
    elif width > 0:
        ratio = width / w
        w, h = width, int(h * ratio)
    elif height > 0:
        ratio = height / h
        w, h = int(w * ratio), height
    img = img.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png",
                             headers={"Content-Disposition": f"attachment; filename=resized_{file.filename}"})

@router.get("/palette", response_class=HTMLResponse)
async def palette_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "tool_image.html", ctx(request, active_tab="palette"))

@router.get("/convert", response_class=HTMLResponse)
async def convert_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "tool_image.html", ctx(request, active_tab="convert"))

@router.get("/resize", response_class=HTMLResponse)
async def resize_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "tool_image.html", ctx(request, active_tab="resize"))
