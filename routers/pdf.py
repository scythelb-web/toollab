from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import io
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from main import ctx

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def pdf_home(request: Request):
    return request.app.state.templates.TemplateResponse("tool_pdf.html", ctx(request))

@router.post("/merge", response_class=StreamingResponse)
async def pdf_merge(request: Request, files: list[UploadFile] = File(...)):
    merger = PdfMerger()
    for f in files:
        merger.append(io.BytesIO(await f.read()))
    buf = io.BytesIO()
    merger.write(buf)
    merger.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=merged.pdf"})

@router.post("/compress")
async def pdf_compress(request: Request, file: UploadFile = File(...)):
    reader = PdfReader(io.BytesIO(await file.read()))
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="application/pdf",
                             headers={"Content-Disposition": f"attachment; filename=compressed_{file.filename}"})

@router.get("/summarize", response_class=HTMLResponse)
async def pdf_summarize_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "tool_pdf.html", ctx(request, active_tab="summarize"))

@router.get("/chat", response_class=HTMLResponse)
async def pdf_chat_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "tool_pdf.html", ctx(request, active_tab="chat"))
