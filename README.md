# Jarvis

Assistente de voz: **áudio → transcrição (faster-whisper) → resposta (Ollama, qwen2.5:1.5b) → voz (Kokoro)**.

## Instalação (Linux)

### 1. Pacotes do sistema

Arch / Manjaro:

```bash
sudo pacman -S --needed python git wget ollama
```

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git wget curl
curl -fsSL https://ollama.com/install.sh | sh
```

Fedora:

```bash
sudo dnf install -y python3 python3-pip git wget curl
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Ollama + modelo de linguagem

```bash
sudo systemctl enable --now ollama
ollama pull qwen2.5:1.5b
```

### 3. Ambiente Python

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.exemplo .env
```

### 4. Modelos de voz do Kokoro

Ficam em `modelos/` (fora do git):

```bash
wget -P modelos https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget -P modelos https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

O modelo do Whisper é baixado sozinho na primeira transcrição.

## Rodar

```bash
.venv/bin/python app.py
```

Abra http://localhost:8000. Na interface dá para gravar pelo microfone, enviar um arquivo de áudio ou digitar.
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
saidas/                 .wav gerados pela interface (ignorado pelo git)
```
