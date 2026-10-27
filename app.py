"""Interface web do Jarvis.  Rode com:  .venv/bin/python app.py  e abra http://localhost:8000"""

import shutil
import tempfile
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from jarvis import agente, config, transcricao, voz

app = FastAPI(title="Jarvis")
app.mount("/saidas", StaticFiles(directory=config.SAIDAS), name="saidas")
app.mount("/static", StaticFiles(directory=config.RAIZ / "static"), name="static")


@app.get("/")
def inicio():
    return FileResponse(config.RAIZ / "static" / "index.html")


@app.get("/api/opcoes")
def opcoes():
    return {
        "whisper_modelos": config.WHISPER_MODELOS_DISPONIVEIS,
        "whisper_padrao": config.WHISPER_MODELO,
        "vozes": voz.vozes(),
        "voz_padrao": config.VOZ_PADRAO,
    }


@app.post("/api/transcrever")
def api_transcrever(audio: UploadFile = File(...), modelo: str = Form(config.WHISPER_MODELO)):
    if modelo not in config.WHISPER_MODELOS_DISPONIVEIS:
        raise HTTPException(400, f"Modelo inválido: {modelo}")
    sufixo = Path(audio.filename or "audio.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(suffix=sufixo, delete=False) as tmp:
        shutil.copyfileobj(audio.file, tmp)
    try:
        return transcricao.transcrever(tmp.name, modelo)
    finally:
        Path(tmp.name).unlink(missing_ok=True)


class Mensagem(BaseModel):
    texto: str
    historico: list[dict] = []


@app.post("/api/responder")
def api_responder(msg: Mensagem):
    try:
        return agente.responder(msg.texto, msg.historico)
    except agente.ErroAgente as e:
        raise HTTPException(502, str(e))


class Fala(BaseModel):
    texto: str
    voz: str = config.VOZ_PADRAO
    velocidade: float = 1.0


@app.post("/api/falar")
def api_falar(fala: Fala):
    resultado = voz.falar(fala.texto, fala.voz, fala.velocidade)
    return {"url": f"/saidas/{resultado['arquivo'].name}", "segundos": resultado["segundos"]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
