"""
Configuração de Exemplo para Uso Local com GPU 2-3GB e Português

Este arquivo mostra como configurar VoxRad para:
- Transcrição local com Whisper (tiny quantizado)
- Formatação com Ollama (Mistral 7B quantizado)
- Idioma: Português Brasileiro

INSTRUÇÕES:
1. Copiar as linhas abaixo
2. Colar em config/config.py (dentro da classe Config)
3. Salvar o arquivo
4. Iniciar Ollama: ollama serve
5. Executar: python VoxRad.py
"""

# ============= CONFIGURAÇÃO PARA 2-3GB VRAM =============

# Local ASR Settings (Transcrição Whisper Local)
ASR_BACKEND = "local"                  # "api" para OpenAI, "local" para Whisper local
WHISPER_MODEL_SIZE = "tiny"            # "tiny" (1.5GB) ou "base" (2.0GB)
WHISPER_QUANTIZATION = "int8"          # "int8" ou "int4" (mais agressivo)
WHISPER_LANGUAGE = "pt"                # Português

# LLM Settings (Formatação com Ollama Local)
SELECTED_MODEL = "mistral:7b-instruct-v0.2-q4_K_M"  # Modelo local quantizado
BASE_URL = "http://localhost:11434/v1"              # Ollama endpoint
TEXT_API_KEY = "ollama"                             # Dummy key para local (não usado)

# ============= ALTERNATIVAS PARA DIFERENTES CASOS =============

"""
OPÇÃO 1: Máximo Performance (Mais Rápido)
- Use se tiver áudio de boa qualidade e quer máxima velocidade
- VRAM: ~2.0GB
"""
# WHISPER_MODEL_SIZE = "tiny"
# SELECTED_MODEL = "neural-chat:7b-v3.3-q4_K_M"  # Muito rápido

"""
OPÇÃO 2: Máxima Qualidade
- Use se tiver ruído ou sotaques regionais
- VRAM: ~2.8GB (no limite, mas funciona)
"""
# WHISPER_MODEL_SIZE = "base"
# SELECTED_MODEL = "dolphin-mixtral:8x7b-v2.1-q4_K_M"  # Mais poderoso

"""
OPÇÃO 3: Equilíbrio
- Use se quer bom custo-benefício
- VRAM: ~2.5GB
"""
# WHISPER_MODEL_SIZE = "tiny"
# SELECTED_MODEL = "mistral:7b-instruct-v0.2-q4_K_M"  # Nosso padrão

# ============= PREPARAÇÃO =============

"""
PASSO 1: Instalar Ollama
- Windows: https://ollama.ai/download
- macOS: https://ollama.ai/download
- Linux: curl https://ollama.ai/install.sh | sh

PASSO 2: Baixar Modelo Quantizado
Abrir Terminal e executar:

    # Para Performance (recomendado)
    ollama pull mistral:7b-instruct-v0.2-q4_K_M

    # Ou para velocidade máxima
    ollama pull neural-chat:7b-v3.3-q4_K_M

    # Ou para qualidade máxima (se tiver 3GB)
    ollama pull dolphin-mixtral:8x7b-v2.1-q4_K_M

PASSO 3: Iniciar Ollama
    # Terminal 1
    ollama serve

    # Terminal 2
    cd /home/user/VoxRad
    python VoxRad.py

PASSO 4: Verificar Funcionamento
- Fale algo em português
- Clique "Transcribe"
- Sistema deve transcrever e formatar automaticamente
- Primeira execução é mais lenta (carrega modelo)
"""

# ============= MODELOS DISPONÍVEIS =============

"""
PARA TRANSCRIÇÃO (Whisper):
- tiny (39M): 1.5GB - Muito rápido, bom para português claro
- base (74M): 2.0GB - Um pouco mais lento, melhor qualidade
❌ small (244M): 4.0GB - Grande demais para seu hardware

PARA FORMATAÇÃO (Ollama):
Quantização Q4 (bom balanço entre qualidade e velocidade)
- neural-chat:7b: 2.4GB - Muito rápido, ótimo para chat
- mistral:7b-instruct: 2.5GB - Excelente qualidade, português bom
- dolphin-mixtral:8x7b: 2.8GB - Melhor qualidade, mais lento

Quantização Q5 (melhor qualidade, mais VRAM):
- mistral:7b-instruct-q5_K_M: 3.0GB - Qualidade superior
- neural-chat:7b-q5_K_M: 2.9GB - Muito bom

❌ Quantização Q6+ ou sem quantização - Requer 4GB+
"""

# ============= TESTES =============

"""
TESTAR TRANSCRIÇÃO LOCAL:
- Settings > Local ASR Settings > ☑ Use Local Whisper
- Clique Record
- Fale: "Olá, como vai?"
- Clique Transcribe
- Deve mostrar: "Olá, como vai?"

TESTAR FORMATAÇÃO LOCAL:
- Settings > Model Selection > Url: http://localhost:11434/v1
- Depois de transcrever, deve formatar automaticamente
- Resultado aparece na caixa de texto

PROBLEMAS:
- Se disser "Connection refused": Ollama não está rodando
  → Terminal: ollama serve

- Se disser "Out of Memory": GPU com pouca memória
  → Usar WHISPER_MODEL_SIZE = "tiny" (1.5GB)
  → Ou usar WHISPER_QUANTIZATION = "int4" (mais comprimido)

- Se transcrição ruim: Áudio com muito ruído
  → Melhorar qualidade do áudio
  → Ou usar WHISPER_MODEL_SIZE = "base" (melhor qualidade)
"""
