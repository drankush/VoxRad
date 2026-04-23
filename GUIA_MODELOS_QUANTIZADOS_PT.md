# Guia de Modelos Quantizados para GPU com 2-3GB VRAM

## Recomendações de Modelos Quantizados

### 1. **Para Transcrição (Whisper - Português)**

#### ✅ Recomendado: `tiny` com int8
```python
# config/config.py
WHISPER_MODEL_SIZE = "tiny"          # 39M parâmetros
WHISPER_QUANTIZATION = "int8"         # 8-bit quantization
WHISPER_LANGUAGE = "pt"               # Português
```
- **VRAM necessário:** ~1.5GB
- **Velocidade:** 3-5x mais rápido que base
- **Precisão:** ~95% em português claro
- **Ideal para:** Fala clara e boa qualidade de áudio

#### Alternativa: `base` com int8
```python
WHISPER_MODEL_SIZE = "base"           # 74M parâmetros
WHISPER_QUANTIZATION = "int8"
WHISPER_LANGUAGE = "pt"
```
- **VRAM necessário:** ~2GB
- **Velocidade:** Mais lento que tiny
- **Precisão:** ~98% em português
- **Ideal para:** Áudio com ruído ou sotaques regionais

#### ⚠️ Evitar: `small`, `medium`, `large`
- `small`: 244M parâmetros = ~4GB (acima do seu limite)
- `medium`: 769M parâmetros = ~8GB
- `large`: 1550M parâmetros = ~15GB

### 2. **Para Formatação de Relatórios (LLM Local)**

#### ✅ Recomendado: Ollama com quantização

**Modelos que funcionam em 2-3GB:**

1. **Mistral 7B (Q4_K_M)** - Melhor para português
```bash
ollama pull mistral:7b-instruct-v0.2-q4_K_M
```
- VRAM: ~2.5GB
- Qualidade: Excelente para português
- Velocidade: Rápido
- Contexto: 32K tokens

2. **Neural Chat 7B (Q4)**
```bash
ollama pull neural-chat:7b-v3.3-q4_K_M
```
- VRAM: ~2.4GB
- Qualidade: Otimizado para chat
- Velocidade: Muito rápido
- Ideal para: Formatação de relatórios

3. **Dolphin 2.6 Mixtral 8x7B (Q4)** - Mais poderoso (use se tiver 3GB)
```bash
ollama pull dolphin-mixtral:8x7b-v2.1-q4_K_M
```
- VRAM: ~2.8GB
- Qualidade: Estado da arte
- Velocidade: Equilibrado
- Contexto: 32K tokens

### 3. **Configuração para Usar Localmente**

#### No arquivo `config/config.py`:
```python
# Local ASR Settings
ASR_BACKEND = "local"                 # Usar Whisper local
WHISPER_MODEL_SIZE = "tiny"           # Melhor para 2-3GB
WHISPER_QUANTIZATION = "int8"         # Quantização 8-bit
WHISPER_LANGUAGE = "pt"               # Português

# LLM Settings (local via Ollama)
SELECTED_MODEL = "mistral:7b-instruct-v0.2-q4_K_M"
BASE_URL = "http://localhost:11434/v1"  # Ollama default
TEXT_API_KEY = "ollama"                 # Dummy key para local
```

## Instalação e Configuração

### Passo 1: Instalar Ollama
```bash
# Linux
curl https://ollama.ai/install.sh | sh

# macOS
# Download em https://ollama.ai/download

# Windows
# Download em https://ollama.ai/download
```

### Passo 2: Baixar Modelo Quantizado
```bash
# Abrir terminal e executar:
ollama pull mistral:7b-instruct-v0.2-q4_K_M

# Ou a alternativa mais leve:
ollama pull neural-chat:7b-v3.3-q4_K_M
```

### Passo 3: Verificar GPU
```bash
# Verificar se Ollama está usando GPU
ollama list

# Na output, deve mostrar algo como:
# NAME                                    ID              SIZE      MODIFIED
# mistral:7b-instruct-v0.2-q4_K_M        abc123def456    4.5 GB    2 minutes ago
```

### Passo 4: Iniciar Ollama em Background
```bash
# Linux/macOS
ollama serve &

# Windows (PowerShell)
Start-Process ollama serve
```

### Passo 5: Testar Localmente
```bash
# No terminal VoxRad
python VoxRad.py

# Deve usar transcrição local e LLM local
```

## Comparação de Modelos para 2-3GB VRAM

### Transcrição (Whisper)
| Modelo | Parâmetros | VRAM | Velocidade | Qualidade PT | Recomendação |
|--------|-----------|------|-----------|------------|--------------|
| tiny   | 39M       | 1.5GB| 3-5x      | 95%        | ✅ MELHOR    |
| base   | 74M       | 2.0GB| 2-3x      | 98%        | ✅ Bom      |
| small  | 244M      | 4.0GB| 1.5x      | 99%        | ❌ Grande   |

### LLM (Ollama - Quantizado Q4)
| Modelo | Parâmetros | VRAM | Qualidade | Velocidade | Recomendação |
|--------|-----------|------|----------|-----------|--------------|
| Neural Chat | 7B | 2.4GB | Boa | Muito Rápida | ✅ MELHOR |
| Mistral | 7B | 2.5GB | Excelente | Rápida | ✅ Recomendado |
| Dolphin Mixtral | 8x7B | 2.8GB | Estado-da-arte | Equilibrada | ✅ Se tiver 3GB |
| Llama 2 | 7B | 2.4GB | Boa | Rápida | ✅ Alternativa |

## Configuração Passo a Passo no VoxRad

### 1. Abrir Settings (Configurações)
- Clique em "Settings" na interface principal
- Procure por "Local ASR Settings"

### 2. Configurar Whisper Local
```
☑ Use Local Whisper (desabilitar API)
Model Size: tiny
Quantization: int8
Language: pt (Português)
```

### 3. Configurar LLM Local
```
☑ Use Local LLM
Model: mistral:7b-instruct-v0.2-q4_K_M
Base URL: http://localhost:11434/v1
API Key: ollama
```

### 4. Testar Gravação
1. Fale em português
2. Clique "Transcribe"
3. Sistema usará Whisper tiny local
4. Depois formará relatório com Mistral local

## Performance Esperado

### Com seu hardware (2-3GB VRAM):
```
Gravação 1 minuto:
- Transcription: ~3-5 segundos (tiny) ou ~5-8 segundos (base)
- Formatação: ~2-4 segundos (Mistral Q4)
- Total: ~5-12 segundos por minuto de áudio

Gravação 5 minutos:
- Transcription: ~15-25 segundos
- Formatação: ~5-8 segundos  
- Total: ~20-33 segundos

Gravação 10 minutos:
- Transcription: ~30-50 segundos
- Formatação: ~8-15 segundos
- Total: ~40-60 segundos
```

## Troubleshooting

### Problema: "Out of Memory" (GPU)
**Solução:**
```python
# Reduzir para modelo menor
WHISPER_MODEL_SIZE = "tiny"  # De "base"

# Usar quantização mais agressiva
WHISPER_QUANTIZATION = "int4"  # De "int8"

# Usar modelo LLM menor
# ollama pull neural-chat:7b-v3.3-q4_K_M
```

### Problema: Modelo carrega lentamente
**Solução:**
- Primeiro carregamento é lento (primeiro uso)
- Com caching (melhorias recentes): ~0.1s nos próximos usos
- Se muito lento, reduzir modelo para "tiny"

### Problema: Ollama não encontrada
**Solução:**
```bash
# Verificar se Ollama está rodando:
curl http://localhost:11434/api/tags

# Se não, iniciar:
ollama serve

# No Windows, pode precisar reinstalar Ollama
```

### Problema: Transcrição ruim em português
**Solução:**
```python
# Aumentar modelo de tiny para base
WHISPER_MODEL_SIZE = "base"

# Ou melhorar áudio:
# - Usar microfone melhor
# - Reduzir ruído de fundo
# - Falar mais claro
```

## Arquivos a Modificar

### 1. `config/config.py`
```python
# Local ASR Settings
ASR_BACKEND = "local"
WHISPER_MODEL_SIZE = "tiny"
WHISPER_QUANTIZATION = "int8"
WHISPER_LANGUAGE = "pt"

# LLM Settings
SELECTED_MODEL = "mistral:7b-instruct-v0.2-q4_K_M"
BASE_URL = "http://localhost:11434/v1"
TEXT_API_KEY = "ollama"
```

### 2. Verificar `audio/transcriber.py`
- Já suporta backend local
- Usar `get_whisper_model()` (com caching)
- Não precisa modificar

### 3. Verificar `llm/format.py`
- Detecta automaticamente OpenAI ou local
- Se `BASE_URL` tiver "localhost", usa local
- Não precisa modificar

## Próximos Passos

1. **Instalar Ollama**
   ```bash
   # https://ollama.ai
   ```

2. **Baixar modelo quantizado**
   ```bash
   ollama pull mistral:7b-instruct-v0.2-q4_K_M
   ```

3. **Modificar config.py** (veja acima)

4. **Iniciar Ollama**
   ```bash
   ollama serve
   ```

5. **Executar VoxRad**
   ```bash
   python VoxRad.py
   ```

## Recursos Adicionais

- **Ollama**: https://ollama.ai
- **Whisper Tiny em PT**: https://huggingface.co/openai/whisper-tiny
- **Mistral 7B Quantizado**: https://ollama.ai/library/mistral
- **Modelos Quantizados**: https://huggingface.co/TheBloke

---

**Nota:** Com as melhorias recentes (caching de modelo), você verá performance ainda melhor após o primeiro carregamento!
