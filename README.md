# Jarvis

Assistente de voz: **áudio → transcrição (faster-whisper) → resposta (Ollama, qwen2.5:1.5b) → voz (Kokoro)**.

## Instalação (Linux)

### 1. Instalar os pacotes do sistema

**Arch Linux / EndeavourOS / Manjaro:**

```bash
sudo pacman -S --needed python git wget ollama
```

**Ubuntu / Debian:**

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git wget curl
curl -fsSL https://ollama.com/install.sh | sh
```

**Fedora:**

```bash
sudo dnf install -y python3 python3-pip git wget curl
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Iniciar o Ollama e baixar o modelo

```bash
sudo systemctl enable --now ollama
ollama pull qwen2.5:1.5b
```

### 3. Configurar o ambiente Python

Na pasta do projeto, execute:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.exemplo .env
```

### 4. Baixar os modelos de voz do Kokoro

Os arquivos devem ficar na pasta `modelos/`, que não é versionada pelo Git.

```bash
wget -P modelos https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget -P modelos https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

O modelo do Whisper é baixado automaticamente na primeira transcrição.

## Executar

```bash
.venv/bin/python app.py
```

Abra http://localhost:8000 no navegador.

Na interface, é possível gravar pelo microfone, enviar um arquivo de áudio ou digitar uma mensagem.

Em **⚙ Configurações**, você pode ajustar o modelo do Whisper, a voz, a velocidade e a reprodução automática (*autoplay*).

## Estrutura do projeto

```text
app.py                  servidor web (FastAPI) + rotas /api/*
static/index.html       interface web

jarvis/
  config.py             caminhos, modelos e .env
  transcricao.py        transcrição com faster-whisper
  agente.py             integração do agente e medição de tempo
  perguntar_ollama.py   prompt do Jarvis + chamada ao Ollama
  voz.py                síntese de voz com Kokoro

modelos/                modelos .onnx e arquivo de vozes
saidas/                 arquivos .wav gerados pela interface
```

**Observações:**
- Os modelos baixados e os arquivos de saída ignorados pelo Git não são incluídos no repositório.
