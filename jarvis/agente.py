import time

from .perguntar_ollama import perguntar_ia


class ErroAgente(Exception):
    pass


def responder(mensagem: str, historico: list[dict] | None = None) -> dict:
    inicio = time.perf_counter()
    try:
        texto = (perguntar_ia(mensagem) or "").strip()
    except Exception as e:
        raise ErroAgente(f"Erro no Ollama: {e}") from e
    if not texto:
        raise ErroAgente("O modelo retornou uma resposta vazia.")
    return {"texto": texto, "segundos": round(time.perf_counter() - inicio, 2)}