import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()
api_key = os.getenv('API_KEY')

if not api_key:
    st.error("⚠️ API_KEY não carregada. Verifique o arquivo .env.")
    st.stop()

def get_groq_completions(user_content):
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente especialista em criar planos de trabalho detalhados para projetos de feira de ciências. Responda sempre em português do Brasil e siga estritamente as instruções de formatação do usuário."
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        temperature=0.7,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

# FUNÇÃO COM LÓGICA DE LIMPEZA CORRIGIDA
def gerar_plano_de_trabalho(dados_usuario):
    prompt = criar_prompt(dados_usuario)
    try:
        response = get_groq_completions(prompt)
        if not response:
            return None

        # Marcador que indica o início de cada seção principal.
        start_marker = "**Propósito de Trabalho:**"
        
        # Usa rfind() para encontrar a ÚLTIMA ocorrência do marcador.
        # Isso garante que pegamos a resposta final e não o preâmbulo/raciocínio do modelo.
        last_marker_pos = response.rfind(start_marker)

        # Se o marcador for encontrado, retorna a string a partir da sua última posição.
        if last_marker_pos != -1:
            return response[last_marker_pos:].strip()
        else:
            # Caso o marcador não seja encontrado, retorna a resposta limpa como fallback.
            return response.strip()

    except Exception as e:
        st.error(f"Erro ao tentar gerar plano de trabalho: {e}")
        return None

# PROMPT REFINADO PARA ELIMINAR O PREÂMBULO
def criar_prompt(dados_usuario):
    metodologia = dados_usuario.get('metodologia')

    instrucao_formato = """
    Crie um plano de trabalho detalhado para um projeto de feira de ciência com o título "{titulo}", cujo objetivo é "{objetivo}" e que utilizará os seguintes materiais: "{materiais}".

    Sua resposta DEVE começar EXATAMENTE com a linha "**Propósito de Trabalho:**". 
    NÃO inclua nenhuma introdução, preâmbulo, explicação ou texto de raciocínio antes do plano de trabalho.
    Siga estritamente o formato Markdown abaixo, com cada seção começando em uma nova linha.
    """

    if metodologia == "Engenharia":
        prompt_template = instrucao_formato + """
        **Propósito de Trabalho:**
        [Nesta seção, explique a razão de ser do projeto, qual problema ou desafio específico pretende abordar, ressaltando os benefícios e contribuições.]

        **Características Físicas e Funcionais:**
        [Detalhe as características do protótipo, explicando como será construído e como suas partes interagem para solucionar o problema proposto.]

        **Restrições/Limitações:**
        [Aborde quaisquer restrições ou limitações que possam afetar o projeto (orçamento, tempo, recursos, tecnologia, etc.).]

        **Avaliação:**
        [Explique os critérios e testes que serão usados para medir o sucesso do projeto (testes de funcionalidade, análises comparativas, etc.).]

        **Cronograma (4 meses):**
        *   **Mês 1:** [Descreva as tarefas principais do primeiro mês]
        *   **Mês 2:** [Descreva as tarefas principais do segundo mês]
        *   **Mês 3:** [Descreva as tarefas principais do terceiro mês]
        *   **Mês 4:** [Descreva as tarefas principais do quarto mês]

        **Bibliografia:**
        *   [Referência 1]
        *   [Referência 2]
        *   [Referência 3]
        """
    elif metodologia == "Científica":
        prompt_template = instrucao_formato + """
        **Propósito de Trabalho:**
        [Explique o objetivo principal da investigação, a pergunta ou problema a ser investigado e o impacto esperado da pesquisa.]

        **Hipótese:**
        [Apresente uma suposição clara e testável sobre os resultados esperados, baseada em conhecimentos prévios.]

        **Método:**
        [Descreva passo a passo os procedimentos que serão seguidos para testar a hipótese, incluindo como os dados serão coletados e controlados.]

        **Análise de Dados:**
        [Explique como os dados coletados serão analisados para confirmar ou refutar a hipótese (uso de gráficos, estatísticas, etc.).]

        **Cronograma (4 meses):**
        *   **Mês 1:** [Descreva as tarefas principais do primeiro mês]
        *   **Mês 2:** [Descreva as tarefas principais do segundo mês]
        *   **Mês 3:** [Descreva as tarefas principais do terceiro mês]
        *   **Mês 4:** [Descreva as tarefas principais do quarto mês]

        **Bibliografia:**
        *   [Referência 1]
        *   [Referência 2]
        *   [Referência 3]
        """
    else:
        return None

    return prompt_template.format(
        titulo=dados_usuario['titulo'],
        objetivo=dados_usuario['objetivo'],
        materiais=dados_usuario['materiais']
    )

# INTERFACE DO STREAMLIT
st.set_page_config(page_title="Lampejo - Plano de Trabalho", page_icon="💡", layout="centered")

st.title("Crie planos de trabalho incríveis com o Lampejo!")
st.subheader("Seu assistente virtual para projetos de pesquisa")

col1, col2, col3 = st.columns([0.2, 1, 0.2])
with col2:
    st.image("lampejo.png")

st.write("""
Com o Lampejo, você tem um assistente inteligente pronto para ajudar na criação de Planos de Trabalho estruturados para seus projetos!
""")

st.info("Para que o Lampejo possa te oferecer o melhor plano, é fundamental que você preencha todas as informações abaixo.")

titulo = st.text_input("Qual é o título do seu projeto?", key="titulo")
objetivo = st.text_area("Qual é o objetivo do seu projeto?", key="objetivo")
materiais = st.text_area("Quais são os principais materiais que você vai utilizar?", key="materiais")
metodologia = st.selectbox("Qual metodologia seu projeto seguirá?", ["", "Científica", "Engenharia"], key="metodologia")

dados_usuario = {
    'titulo': titulo,
    'objetivo': objetivo,
    'materiais': materiais,
    'metodologia': metodologia
}

if st.button("Gerar Plano de Trabalho", type="primary"):
    if not all([titulo, objetivo, materiais, metodologia]):
        st.error("Por favor, preencha todos os campos para continuar.")
    else:
        with st.spinner("Lampejo está organizando as ideias e montando seu plano... aguarde! 💡"):
            response = gerar_plano_de_trabalho(dados_usuario)
        
        st.success("Pronto! Aqui está a sugestão de Plano de Trabalho:")
        if response:
            st.markdown(response)
        else:
            st.warning("Não foi possível gerar o plano. Tente refinar suas respostas ou tente novamente.")
