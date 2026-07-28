from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from openai import OpenAI
import io
from main import ctx

router = APIRouter()

def get_client(request: Request) -> OpenAI | None:
    key = request.session.get("openai_key")
    return OpenAI(api_key=key) if key else None

@router.get("/", response_class=HTMLResponse)
async def voice_home(request: Request):
    return request.app.state.templates.TemplateResponse("tool_voice.html", ctx(request))

@router.post("/tts", response_class=StreamingResponse)
async def text_to_speech(request: Request, text: str = Form(...), voice: str = Form("alloy")):
    client = get_client(request)
    if not client:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse("Set your OpenAI API key in Account settings first.", status_code=401)
    resp = client.audio.speech.create(model="tts-1", voice=voice, input=text)
    return StreamingResponse(io.BytesIO(resp.content), media_type="audio/mpeg",
                             headers={"Content-Disposition": "attachment; filename=speech.mp3"})

@router.post("/stt")
async def speech_to_text(request: Request, file: UploadFile = File(...)):
    client = get_client(request)
    if not client:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse("Set your OpenAI API key in Account settings first.", status_code=401)
    content = await file.read()
    audio_file = io.BytesIO(content)
    audio_file.name = file.filename or "audio.mp3"
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return {"text": transcript.text}
