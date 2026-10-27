import threading
import time
from pathlib import Path

from faster_whisper import WhisperModel

from . import config

_modelos: dict[str, WhisperModel] = {}
_trava = threading.Lock()


def _modelo(nome: str) -> WhisperModel:
    with _trava:
        if nome not in _modelos:
            _modelos[nome] = WhisperModel(nome, device="cpu", compute_type="int8")
        return _modelos[nome]


def transcrever(audio: Path | str, modelo: str = config.WHISPER_MODELO) -> dict:
    """Transcreve um arquivo de áudio. Retorna {"texto", "segundos"}."""
    whisper = _modelo(modelo)
    inicio = time.perf_counter()
    segmentos, _ = whisper.transcribe(str(audio), language=config.WHISPER_IDIOMA)
    texto = " ".join(s.text.strip() for s in segmentos).strip()
    return {"texto": texto, "segundos": round(time.perf_counter() - inicio, 2)}
