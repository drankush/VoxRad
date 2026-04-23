#!/bin/bash

# Script de Configuração Rápida para VoxRad Local em Português
# Uso: bash setup_local_modelo_pt.sh

echo "=========================================="
echo "VoxRad - Configurador de Modelos Locais PT"
echo "=========================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado"
    echo "Instale Python 3.8 ou superior"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verificar se Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama não encontrado"
    echo "Download em https://ollama.ai"
    echo "Você precisará iniciar Ollama manualmente: ollama serve"
    echo ""
else
    echo "✅ Ollama encontrado"
    echo ""
fi

# Menu de seleção
echo "Escolha uma opção:"
echo ""
echo "1) Configuração Rápida (Mistral 7B - Recomendado)"
echo "2) Máxima Performance (Neural Chat - Mais rápido)"
echo "3) Máxima Qualidade (Dolphin Mixtral - Melhor)"
echo "4) Baixar Modelos Ollama"
echo "5) Testar Conexão com Ollama"
echo ""
read -p "Opção (1-5): " opcao

case $opcao in
    1)
        echo ""
        echo "📝 Configurando para Mistral 7B..."
        echo ""

        # Criar backup
        if [ -f "config/config.py" ]; then
            cp config/config.py config/config.py.backup
            echo "✅ Backup criado: config/config.py.backup"
        fi

        # Adicionar configuração
        cat >> config/config.py << 'EOF'

# ===== CONFIGURAÇÃO LOCAL PT (MISTRAL 7B) =====
# Configurado por setup_local_modelo_pt.sh
ASR_BACKEND = "local"
WHISPER_MODEL_SIZE = "tiny"
WHISPER_QUANTIZATION = "int8"
WHISPER_LANGUAGE = "pt"
SELECTED_MODEL = "mistral:7b-instruct-v0.2-q4_K_M"
BASE_URL = "http://localhost:11434/v1"
TEXT_API_KEY = "ollama"
EOF

        echo "✅ Configuração adicionada!"
        echo ""
        echo "Próximos passos:"
        echo "1. Abra um terminal e execute: ollama pull mistral:7b-instruct-v0.2-q4_K_M"
        echo "2. Depois execute: ollama serve"
        echo "3. Em outro terminal, execute: python VoxRad.py"
        ;;

    2)
        echo ""
        echo "📝 Configurando para Neural Chat (Performance)..."
        echo ""

        if [ -f "config/config.py" ]; then
            cp config/config.py config/config.py.backup
            echo "✅ Backup criado"
        fi

        cat >> config/config.py << 'EOF'

# ===== CONFIGURAÇÃO LOCAL PT (NEURAL CHAT) =====
ASR_BACKEND = "local"
WHISPER_MODEL_SIZE = "tiny"
WHISPER_QUANTIZATION = "int8"
WHISPER_LANGUAGE = "pt"
SELECTED_MODEL = "neural-chat:7b-v3.3-q4_K_M"
BASE_URL = "http://localhost:11434/v1"
TEXT_API_KEY = "ollama"
EOF

        echo "✅ Configuração adicionada!"
        echo ""
        echo "Próximos passos:"
        echo "1. ollama pull neural-chat:7b-v3.3-q4_K_M"
        echo "2. ollama serve"
        echo "3. python VoxRad.py"
        ;;

    3)
        echo ""
        echo "📝 Configurando para Dolphin Mixtral (Qualidade Máxima)..."
        echo ""

        if [ -f "config/config.py" ]; then
            cp config/config.py config/config.py.backup
            echo "✅ Backup criado"
        fi

        cat >> config/config.py << 'EOF'

# ===== CONFIGURAÇÃO LOCAL PT (DOLPHIN MIXTRAL) =====
ASR_BACKEND = "local"
WHISPER_MODEL_SIZE = "base"
WHISPER_QUANTIZATION = "int8"
WHISPER_LANGUAGE = "pt"
SELECTED_MODEL = "dolphin-mixtral:8x7b-v2.1-q4_K_M"
BASE_URL = "http://localhost:11434/v1"
TEXT_API_KEY = "ollama"
EOF

        echo "✅ Configuração adicionada!"
        echo ""
        echo "⚠️  Nota: Usa 2.8GB VRAM - No limite do seu hardware"
        echo ""
        echo "Próximos passos:"
        echo "1. ollama pull dolphin-mixtral:8x7b-v2.1-q4_K_M"
        echo "2. ollama serve"
        echo "3. python VoxRad.py"
        ;;

    4)
        echo ""
        echo "📥 Baixando modelos Ollama..."
        echo ""

        if ! command -v ollama &> /dev/null; then
            echo "❌ Ollama não está instalado"
            echo "Instale em https://ollama.ai"
            exit 1
        fi

        echo "Qual modelo deseja baixar?"
        echo "1) Mistral 7B (Recomendado)"
        echo "2) Neural Chat (Performance)"
        echo "3) Dolphin Mixtral (Qualidade Máxima)"
        read -p "Opção: " model_choice

        case $model_choice in
            1)
                echo ""
                echo "Baixando Mistral 7B..."
                ollama pull mistral:7b-instruct-v0.2-q4_K_M
                ;;
            2)
                echo ""
                echo "Baixando Neural Chat..."
                ollama pull neural-chat:7b-v3.3-q4_K_M
                ;;
            3)
                echo ""
                echo "Baixando Dolphin Mixtral..."
                ollama pull dolphin-mixtral:8x7b-v2.1-q4_K_M
                ;;
            *)
                echo "Opção inválida"
                ;;
        esac
        ;;

    5)
        echo ""
        echo "🔍 Testando conexão com Ollama..."
        echo ""

        if curl -s http://localhost:11434/api/tags > /dev/null; then
            echo "✅ Ollama está respondendo!"
            echo ""
            echo "Modelos disponíveis:"
            curl -s http://localhost:11434/api/tags | python3 -m json.tool 2>/dev/null || curl -s http://localhost:11434/api/tags
        else
            echo "❌ Ollama não está respondendo"
            echo ""
            echo "Verifique se Ollama está rodando:"
            echo "1. Abra um terminal"
            echo "2. Execute: ollama serve"
            echo "3. Tente novamente"
        fi
        ;;

    *)
        echo "Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Configuração concluída!"
echo "=========================================="
