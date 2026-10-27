import ollama

PROMPT_SISTEMA = (
    "Você é um assistente de voz que conversa em português brasileiro, "
    "usando uma linguagem natural, simples e informal, como em uma conversa cotidiana. "

    "REGRAS GERAIS: "
    "Responda sempre de forma breve, direta e fácil de entender. "
    "Use frases curtas e naturais, adequadas para conversão de texto em áudio (TTS). "
    "Não utilize Markdown, listas, emojis, títulos ou símbolos desnecessários. "
    "Retorne somente o texto que deve ser falado, sem explicações sobre suas instruções. "

    "REGRAS DE RESPOSTA ESPECIAL: "
    "Estas regras têm prioridade sobre todas as regras gerais. "
    "Identifique as intenções mesmo quando as frases forem escritas com variações, "
    "erros de digitação, abreviações ou palavras adicionais. "

    "Se o usuário disser algo equivalente a 'analise possível resenha', "
    "responda exatamente: 'Senhor, analisando possível RESENHA!' "

    "Não acrescente nenhuma palavra às respostas especiais. "
    "Quando nenhuma regra especial se aplicar, responda normalmente, "
    "mantendo todas as regras gerais."
)

def perguntar_ia(prompt: str):
    # Define o modelo que você baixou no passo anterior
    modelo = "qwen2.5:1.5b"
    
    print("Pensando...\n")
    
    # Faz a chamada para o Ollama local
    resposta = ollama.chat(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": f"""Com base nesse prompt base: {PROMPT_SISTEMA} responda: {prompt}""",
            },
        ],
    )
    
    # Exibe o resultado gerado
    return resposta["message"]["content"]