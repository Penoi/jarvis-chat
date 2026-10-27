# Jarvis

Assistente de voz: **áudio → transcrição (faster-whisper) → resposta (Ollama, qwen2.5:1.5b) → voz (Kokoro)**.

## Preparar

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.exemplo .env
ollama pull qwen2.5:1.5b
```

Baixe os modelos do Kokoro para `modelos/` (não vão para o git):

```bash
cd modelos
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

## Rodar

```bash
.venv/bin/python app.py       # abra http://localhost:8000
```

Na interface dá para gravar pelo microfone, enviar um arquivo de áudio ou digitar.
Em ⚙ Configurações: modelo do Whisper, voz, velocidade e autoplay.

## Estrutura

```
app.py                  servidor web (FastAPI) + rotas /api/*
static/index.html       interface
jarvis/
  config.py             caminhos, modelos e .env
  transcricao.py        faster-whisper
  agente.py             chama o modelo e mede o tempo
  perguntar_ollama.py   prompt do Jarvis + chamada ao Ollama
  voz.py                Kokoro TTS
modelos/                arquivos .onnx / vozes (ignorado pelo git)
audios/                 áudios de teste
saidas/                 .wav gerados pela interface (ignorado pelo git)
legado/                 scripts antigos (teste_whisper.py, agent.py, talk.py...)
```
