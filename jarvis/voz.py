import threading
import time
import uuid
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro

from . import config

_kokoro: Kokoro | None = None
_trava = threading.Lock()


def _modelo() -> Kokoro:
    global _kokoro
    with _trava:
        if _kokoro is None:
            _kokoro = Kokoro(str(config.KOKORO_MODELO), str(config.KOKORO_VOZES))
        return _kokoro


def vozes() -> list[str]:
    return sorted(_modelo().get_voices())


def falar(texto: str, voz: str = config.VOZ_PADRAO, velocidade: float = 1.0) -> dict:
    """Gera um .wav em saidas/. Retorna {"arquivo": Path, "segundos"}."""
    kokoro = _modelo()
    inicio = time.perf_counter()
    # pf_/pm_ são as vozes em português; as demais usam o sotaque de origem
    idioma = "pt-br" if voz.startswith("p") else "en-us"
    amostras, taxa = kokoro.create(text=texto, voice=voz, speed=velocidade, lang=idioma)
    arquivo: Path = config.SAIDAS / f"jarvis_{uuid.uuid4().hex[:8]}.wav"
    sf.write(arquivo, amostras, taxa)
    return {"arquivo": arquivo, "segundos": round(time.perf_counter() - inicio, 2)}
