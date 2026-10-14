import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações do Modelo Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash"
FALLBACK_MODEL_NAME = "gemini-3.8-flash-lite"  # Usado se o principal der erro 503/500

# Configurações de Histórico e Conversa
MAX_HISTORY_TURNS = 10  # Mantém até 10 pares (user + model)
APPROX_CHARS_PER_TOKEN = 4  # Estimativa aproximada para contagem de tokens

# Configurações de Resiliência (Retries & Exponential Backoff)
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2.0  # Segundos
BACKOFF_FACTOR = 2.0