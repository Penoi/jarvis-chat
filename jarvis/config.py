import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = RAIZ / "modelos"
SAIDAS = RAIZ / "saidas"
SAIDAS.mkdir(exist_ok=True)


def _carregar_env():
    """Lê variáveis de um arquivo .env na raiz (ex.: GEMINI_API_KEY=...)."""
    arquivo = RAIZ / ".env"
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


_carregar_env()

# Transcrição (faster-whisper)
WHISPER_MODELO = os.getenv("WHISPER_MODELO", "small")
WHISPER_MODELOS_DISPONIVEIS = ["base", "small", "medium", "large-v3"]
WHISPER_IDIOMA = "pt"


# Voz (Kokoro)
KOKORO_MODELO = MODELOS / "kokoro-v1.0.onnx"
KOKORO_VOZES = MODELOS / "voices-v1.0.bin"
VOZ_PADRAO = "pf_dora"
