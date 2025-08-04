import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()
api_key = "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"

if not api_key:
    st.error("⚠️ API_KEY não carregada. Verifique o arquivo .env.")
    st.stop()

def get_groq_completions(user_content):
    """
    Função que se conecta à API da Groq para obter a resposta do modelo.
    """
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-70b-8192", # Mudei para um modelo mais robusto para instruções
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente especialista em criar planos de trabalho detalhados para projetos de feira de ciências. Responda sempre em português do Brasil. Siga estritamente a estrutura e o formato solicitados pelo usuário, sem adicionar nenhum texto, introdução ou raciocínio extra."
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
    except Exception as e:
        st.error(f"Erro na comunicação com a API: {e}")
        return None

# PROMPT REFINADO PARA SER MAIS DIRETO E EVITAR CONFUSÃO
def criar_prompt(dados_usuario):
    """
    Cria o prompt final para a IA, com instruções claras e sem ambiguidades.
    """
    metodologia = dados_usuario.get('metodologia')

    # Instrução base clara, separando os dados do formato
    instrucao_base = """
Com base nas informações do projeto a seguir, gere um plano de trabalho detalhado em Português do Brasil.

**Informações do Projeto:**
*   **Título:** {titulo}
*   **Objetivo:** {objetivo}
*   **Materiais:** {materiais}

**Formato Obrigatório:**
Sua resposta DEVE começar EXATAMENTE com "**Propósito de Trabalho:**" e seguir estritamente a estrutura de Markdown abaixo. Não adicione NENHUMA introdução, explicação ou texto de raciocínio antes do plano. Preencha cada seção com conteúdo relevante e detalhado para o projeto.
"""

    if metodologia == "Engenharia":
        # Estrutura limpa, sem instruções confusas nos colchetes
        estrutura = """
**Propósito de Trabalho:**
**Características Físicas e Funcionais:**
**Restrições/Limitações:**
**Avaliação:**
**Cronograma (4 meses):**
*   **Mês 1:** 
*   **Mês 2:** 
*   **Mês 3:** 
*   **Mês 4:** 
**Bibliografia:**
*   [Referência 1]
*   [Referência 2]
*   [Referência 3]
"""
    elif metodologia == "Científica":
        # Estrutura limpa, sem instruções confusas nos colchetes
        estrutura = """
**Propósito de Trabalho:**
**Hipótese:**
**Método:**
**Análise de Dados:**
**Cronograma (4 meses):**
*   **Mês 1:** 
*   **Mês 2:** 
*   **Mês 3:** 
*   **Mês 4:** 
**Bibliografia:**
*   [Referência 1]
*   [Referência 2]
*   [Referência 3]
"""
    else:
        return None

    prompt_template = instrucao_base + estrutura
    return prompt_template.format(
        titulo=dados_usuario['titulo'],
        objetivo=dados_usuario['objetivo'],
        materiais=dados_usuario['materiais']
    )

# FUNÇÃO DE GERAÇÃO E LIMPEZA COM LÓGICA ROBUSTA
def gerar_plano_de_trabalho(dados_usuario):
    """
    Orquestra a criação do prompt, a chamada à API e a limpeza da resposta.
    """
    prompt = criar_prompt(dados_usuario)
    if not prompt:
        st.error("Metodologia inválida.")
        return None
        
    try:
        response = get_groq_completions(prompt)
        if not response:
            return None

        # Marcador que indica o início real do conteúdo.
        start_marker = "**Propósito de Trabalho:**"
        
        # Usa rfind() para encontrar a ÚLTIMA ocorrência do marcador.
        # Isso garante que pegamos a resposta final e não um possível preâmbulo/raciocínio do modelo.
        last_marker_pos = response.rfind(start_marker)

        # Se o marcador for encontrado, retorna a string a partir da sua última posição.
        if last_marker_pos != -1:
            return response[last_marker_pos:].strip()
        else:
            # Caso o marcador não seja encontrado (improvável com o novo prompt), 
            # retorna a resposta inteira como fallback.
            return response.strip()

    except Exception as e:
        st.error(f"Erro ao tentar gerar plano de trabalho: {e}")
        return None

# --- INTERFACE DO STREAMLIT (Nenhuma alteração necessária aqui) ---

st.set_page_config(page_title="Lampejo - Plano de Trabalho", page_icon="💡", layout="centered")

st.title("Crie planos de trabalho incríveis com o Lampejo!")
st.subheader("Seu assistente virtual para projetos de pesquisa")

col1, col2, col3 = st.columns([0.2, 1, 0.2])
with col2:
    # Use um try-except para a imagem, caso ela não seja encontrada
    try:
        st.image("lampejo.png")
    except Exception:
        st.info("💡")

st.write("""
Com o Lampejo, você tem um assistente inteligente pronto para ajudar na criação de Planos de Trabalho estruturados para seus projetos!
""")

st.info("Para que o Lampejo possa te oferecer o melhor plano, é fundamental que você preencha todas as informações abaixo.")

# Usando um formulário para agrupar os inputs
with st.form(key="project_form"):
    titulo = st.text_input("Qual é o título do seu projeto?", key="titulo")
    objetivo = st.text_area("Qual é o objetivo do seu projeto?", key="objetivo", height=100)
    materiais = st.text_area("Quais são os principais materiais que você vai utilizar?", key="materiais", height=100)
    metodologia = st.selectbox("Qual metodologia seu projeto seguirá?", ["", "Científica", "Engenharia"], key="metodologia")

    # Botão de submissão do formulário
    submitted = st.form_submit_button("Gerar Plano de Trabalho", type="primary")

if submitted:
    if not all([titulo, objetivo, materiais, metodologia]):
        st.error("Por favor, preencha todos os campos para continuar.")
    else:
        dados_usuario = {
            'titulo': titulo,
            'objetivo': objetivo,
            'materiais': materiais,
            'metodologia': metodologia
        }
        with st.spinner("Lampejo está organizando as ideias e montando seu plano... aguarde! 💡"):
            response = gerar_plano_de_trabalho(dados_usuario)
        
        if response:
            st.success("Pronto! Aqui está a sugestão de Plano de Trabalho:")
            st.markdown(response)
        else:
            st.warning("Não foi possível gerar o plano. Tente refinar suas respostas ou tente novamente.")
