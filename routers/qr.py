"""QR code generator."""
import io
import qrcode
from qrcode.image.styledpil import StyledPilImage
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from context import ctx

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def qr_home(request: Request):
    return request.app.state.templates.TemplateResponse("tool_qr.html", ctx(request))


@router.post("/generate")
async def generate_qr(request: Request, text: str = Form(...), size: int = Form(300)):
    """Generate a QR code PNG from text."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    if size != 300:
        ratio = size / img.size[0]
        img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png",
                             headers={"Content-Disposition": "attachment; filename=qrcode.png"})
