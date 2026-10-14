import sys
from chatbot import GeminiChatbot, ConversationManager
from prompts import (
    SYSTEM_PROMPT,
    get_concept_explanation_prompt,
    get_practice_question_prompt,
    get_feedback_prompt,
)


def print_help():
    print("""
=== COMANDOS DISPONÍVEIS ===
  help      - Exibe esta mensagem de ajuda
  explain   - Solicita explicação guiada de um conceito
  practice  - Gera uma questão prática guiada
  feedback  - Pede avaliação/feedback para a sua resposta de um exercício
  summary   - Exibe a contagem de mensagens e uso aproximado de tokens
  clear     - Limpa o histórico atual de conversa
  quit/exit - Encerra o assistente de estudos
""")


def handle_explain_cmd(chatbot: GeminiChatbot, conversation: ConversationManager):
    print("\n--- Explicação de Conceito ---")
    conceito = input("Digite o conceito (ex: Polimorfismo): ").strip()
    disciplina = input("Digite a disciplina (ex: Programação Java): ").strip()
    nivel = input("Digite seu nível (ex: Iniciante, Universitário): ").strip() or "Universitário"

    if not conceito or not disciplina:
        print("[Erro] Conceito e Disciplina são obrigatórios.")
        return

    prompt = get_concept_explanation_prompt(conceito, nivel, disciplina)
    _execute_stream(chatbot, prompt, conversation)


def handle_practice_cmd(chatbot: GeminiChatbot, conversation: ConversationManager):
    print("\n--- Gerar Questão Prática ---")
    tema = input("Digite o tema da questão (ex: Recursão): ").strip()
    disciplina = input("Digite a disciplina (ex: Estruturas de Dados): ").strip()
    nivel = input("Digite o nível (ex: Básico, Intermediário): ").strip() or "Intermediário"

    if not tema or not disciplina:
        print("[Erro] Tema e Disciplina são obrigatórios.")
        return

    prompt = get_practice_question_prompt(disciplina, tema, nivel)
    _execute_stream(chatbot, prompt, conversation)


def handle_feedback_cmd(chatbot: GeminiChatbot, conversation: ConversationManager):
    print("\n--- Avaliação de Resposta ---")
    exercicio = input("Digite/Cole o enunciado do exercício: ").strip()
    resposta = input("Digite a sua resposta/resolução: ").strip()

    if not exercicio or not resposta:
        print("[Erro] Exercício e Resposta são obrigatórios.")
        return

    prompt = get_feedback_prompt(exercicio, resposta)
    _execute_stream(chatbot, prompt, conversation)


def _execute_stream(chatbot: GeminiChatbot, prompt: str, conversation: ConversationManager):
    """Auxiliar para executar a chamada e imprimir o fluxo streaming no terminal."""
    print("\nSora (AI): ", end="", flush=True)
    try:
        for chunk in chatbot.stream_response(prompt, conversation):
            print(chunk, end="", flush=True)
        print("\n")
    except Exception as e:
        print(f"\n\n[Erro na execução]: {e}\n")


def main():
    try:
        chatbot = GeminiChatbot()
    except ValueError as err:
        print(f"\n{err}\n")
        sys.exit(1)

    conversation = ConversationManager()

    print("\n==================================================")
    print("      SORA - ASSISTENTE DE ESTUDOS COM AI         ")
    print("==================================================")
    print("Digite 'help' para ver os comandos ou faça uma pergunta diretamente.\n")

    while True:
        try:
            user_input = input("Você > ").strip()

            if not user_input:
                continue

            cmd = user_input.lower()

            if cmd in ["quit", "exit"]:
                print("\nBons estudos! Até a próxima!\n")
                break

            elif cmd == "help":
                print_help()

            elif cmd == "clear":
                conversation.clear()
                print("\n[Histórico de conversa limpo com sucesso!]\n")

            elif cmd == "summary":
                summary = conversation.get_summary()
                print("\n=== RESUMO DA SESSÃO ATUAL ===")
                print(f"- Total de mensagens: {summary['total_messages']}")
                print(f"  - Usuário: {summary['user_messages']}")
                print(f"  - Assistente: {summary['assistant_messages']}")
                print(f"- Estimativa de Tokens Usados: ~{summary['approx_tokens']} tokens\n")

            elif cmd == "explain":
                handle_explain_cmd(chatbot, conversation)

            elif cmd == "practice":
                handle_practice_cmd(chatbot, conversation)

            elif cmd == "feedback":
                handle_feedback_cmd(chatbot, conversation)

            else:
                # Pergunta/mensagem livre do usuário
                _execute_stream(chatbot, user_input, conversation)

        except (KeyboardInterrupt, EOFError):
            print("\n\nSessão encerrada pelo usuário. Até mais!\n")
            break


if __name__ == "__main__":
    main()