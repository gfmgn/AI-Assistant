SYSTEM_PROMPT = """
Você é uma Assistente de Estudos com Inteligência Artificial projetada para ajudar estudantes a aprender de forma eficiente, clara e engajante. Seu objetivo não é apenas fornecer respostas prontas, mas guiar o usuário na compreensão profunda dos conceitos, atuando como uma tutora adaptativa e acessível.
"""

def get_concept_explanation_prompt(conceito: str, nivel: str, disciplina: str) -> str:
    """Gera o prompt para explicação clara e didática de conceitos."""
    return f"""
# TAREFA
Explique o conceito de "{conceito}" para um estudante de nível {nivel}.

# INSTRUÇÕES
1. **Resumo Direto:** Defina o conceito em 1-2 frases simples.
2. **Analogia Prática:** Use uma metáfora intuitiva do mundo real.
3. **Funcionamento Chave:** Destaque os pilares fundamentais em tópicos (bullet points).
4. **Exemplo Aplicado:** Apresente um cenário ou trecho prático em {disciplina}.
5. **Checagem Rápida:** Termine com uma Pergunta de Checagem simples para o estudante responder.
""".strip()


def get_practice_question_prompt(disciplina: str, tema: str, nivel: str) -> str:
    """Gera o prompt para criar uma questão prática guiada."""
    return f"""
# TAREFA
Crie um exercício prático sobre "{tema}" na matéria de {disciplina} (nível {nivel}).

# INSTRUÇÕES
1. **Enunciado Claro:** Apresente a questão de forma objetiva.
2. **Contexto:** Dê os dados ou cenário inicial necessários.
3. **Dica Inicial:** Dê uma dica sutil do caminho/método a seguir, sem dar a resposta.
4. **Pergunte ao Aluno:** Peça para o aluno tentar resolver o primeiro passo.
""".strip()


def get_feedback_prompt(exercicio: str, resposta_usuario: str) -> str:
    """Gera o prompt para avaliar a resposta do usuário a um exercício."""
    return f"""
# TAREFA
Avalie a resposta do estudante para a seguinte questão:

**Exercício:** {exercicio}
**Resposta do Estudante:** {resposta_usuario}

# INSTRUÇÕES
1. **Diagnóstico:** Indique se a resposta está Correta, Parcialmente Correta ou Incorreta.
2. **Análise:** Elogie acertos e identifique onde ocorreu o erro (se houver).
3. **Explicação Passo a Passo:** Mostre como chegar à solução correta.
4. **Próximo Passo:** Faça uma pergunta de acompanhamento para fixação.
""".strip()