import time
from typing import Iterator, List, Dict, Any, Optional
from google import genai
from google.genai import types
from google.genai.errors import APIError

import config
from prompts import SYSTEM_PROMPT


class ConversationManager:
    """Gerencia o histórico de mensagens e cálculo aproximado de tokens."""

    def __init__(self, max_turns: int = config.MAX_HISTORY_TURNS):
        self.max_history_length = max_turns * 2
        self.history: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str) -> None:
        """Adiciona mensagem formatada ao histórico."""
        formatted_role = "user" if role in ["user", "human"] else "model"
        self.history.append({"role": formatted_role, "parts": [{"text": content}]})
        self._trim_history()

    def _trim_history(self) -> None:
        """Corta mensagens antigas mantendo o limite configurado."""
        if len(self.history) > self.max_history_length:
            self.history = self.history[-self.max_history_length:]

    def clear(self) -> None:
        """Limpa o histórico de conversas."""
        self.history.clear()

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def get_summary(self) -> Dict[str, Any]:
        """Calcula o total de mensagens e estimativa de tokens."""
        total_messages = len(self.history)
        total_chars = sum(
            len(part["text"])
            for msg in self.history
            for part in msg.get("parts", [])
        )
        approx_tokens = total_chars // config.APPROX_CHARS_PER_TOKEN

        return {
            "total_messages": total_messages,
            "user_messages": sum(1 for m in self.history if m["role"] == "user"),
            "assistant_messages": sum(1 for m in self.history if m["role"] == "model"),
            "approx_tokens": approx_tokens,
        }


class GeminiChatbot:
    """Cliente wrapper para comunicação resiliente e em streaming com a Gemini API."""

    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "ERRO: GEMINI_API_KEY não encontrada! Configure o arquivo .env ou a variável de ambiente."
            )
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

    def stream_response(
        self,
        prompt: str,
        conversation: ConversationManager,
        system_instruction: str = SYSTEM_PROMPT,
    ) -> Iterator[str]:
        """Envia mensagem e gera resposta streaming com retries (Backoff Exponencial)."""
        if not prompt or not prompt.strip():
            raise ValueError("O prompt enviado não pode estar vazio.")

        contents = []
        contents.extend(conversation.get_history())
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        req_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )

        delay = config.INITIAL_RETRY_DELAY
        full_response_text = ""

        for attempt in range(1, config.MAX_RETRIES + 1):
            try:
                response_stream = self.client.models.generate_content_stream(
                    model=config.MODEL_NAME,
                    contents=contents,
                    config=req_config,
                )

                for chunk in response_stream:
                    chunk_text = chunk.text or ""
                    full_response_text += chunk_text
                    yield chunk_text

                # Sucesso: Adiciona ao histórico do gerenciador
                conversation.add_message("user", prompt)
                conversation.add_message("model", full_response_text)
                return

            except APIError as e:
                if attempt == config.MAX_RETRIES:
                    raise RuntimeError(
                        f"Falha na API após {config.MAX_RETRIES} tentativas. Erro: {e.message}"
                    ) from e
                
                print(f"\n[Aviso: Erro temporário/Rate limit na API ({e.code}). Tentativa {attempt}/{config.MAX_RETRIES}. Aguardando {delay:.1f}s...]")
                time.sleep(delay)
                delay *= config.BACKOFF_FACTOR

            except Exception as e:
                raise RuntimeError(f"Erro inesperado durante comunicação com o Gemini: {str(e)}") from e