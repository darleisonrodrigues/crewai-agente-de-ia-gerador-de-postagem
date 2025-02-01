import os
from groq import Groq
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Carregar variáveis do ambiente
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 🔑 Configurar chave da OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

criador_conteudo = Agent(
    role="Especialista em LinkedIn",
    goal="Criar postagens informativas e profissionais com tópicos bem desenvolvidos.",
    backstory="Especialista em criar postagens virais e envolventes para redes sociais.",
    verbose=True
)

revisor = Agent(
    role="Editor de Conteúdo",
    goal="Otimizar o conteúdo, garantindo clareza, gramática e fluidez.",
    backstory="Editor experiente que transforma postagens simples em conteúdos envolventes.",
    verbose=True
)

formatador = Agent(
    role="Especialista em Formatação",
    goal="Estruturar o post de forma organizada, mantendo a estética e legibilidade.",
    backstory="Especialista em melhorar a legibilidade e a estrutura visual do texto.",
    verbose=True
)

task_criar = Task(
    description=(
        "Escreva uma postagem criativa e envolvente sobre {tema}. "
        "Cada tópico deve conter exatamente 5 linhas para manter um bom equilíbrio entre clareza e profundidade. "
        "O formato da postagem deve ser o seguinte:\n\n"
        "# 🚀 Título chamativo\n\n"
        "💡 Introdução curta e impactante (máximo de 3 linhas)\n\n"
        "1️⃣ Dica 1 - Explicação com exatamente 5 linhas\n"
        "2️⃣ Dica 2 - Explicação com exatamente 5 linhas\n"
        "3️⃣ Dica 3 - Explicação com exatamente 5 linhas\n\n"
        "🔥 Chamada final para ação\n\n"
        "#HashtagsRelevantes"
    ),
    expected_output="Uma postagem formatada com tópicos de exatamente 5 linhas.",
    agent=criador_conteudo
)

task_revisar = Task(
    description=(
        "Revise a postagem e garanta que:\n"
        "- Todos os parágrafos seguem as regras de tamanho.\n"
        "- Os tópicos possuem **exatamente 5 linhas**.\n"
        "- A linguagem seja natural, envolvente e clara.\n"
        "- Nenhum parágrafo esteja muito longo ou curto.\n"
        "- Os emojis e hashtags estejam bem distribuídos."
    ),
    expected_output="Post revisado, garantindo que cada tópico tenha exatamente 5 linhas.",
    agent=revisor
)

task_formatar = Task(
    description=(
        "Formate o post para que ele seja visualmente agradável e bem estruturado.\n"
        "- Mantenha o formato correto sem alterar o número de linhas dos tópicos.\n"
        "- Certifique-se de que cada seção tem espaçamento adequado.\n"
        "- Não use negrito (**), itálico (*) ou qualquer outra marcação especial.\n"
        "- Deixe a postagem com um aspecto profissional e limpo."
    ),
    expected_output="Post formatado com espaçamento correto e estrutura profissional.",
    agent=formatador
)

crew = Crew(
    agents=[criador_conteudo, revisor, formatador],
    tasks=[task_criar, task_revisar, task_formatar],
    process=Process.sequential
)

def gerar_publicacao(tema):
    return str(crew.kickoff(inputs={"tema": tema}))
