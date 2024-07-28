import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv


# Carregar variáveis do arquivo .env
load_dotenv()

# Função para obter as respostas do Groq
def get_groq_completions(user_content):
    client = Groq(
        api_key=os.getenv('API_KEY')
    )

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": user_content + "\nPor favor, responda em português do Brasil."
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        temperature=0.5,
        max_tokens=5640,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

# Função para gerar plano de trabalho de projetos de feira de ciências
def gerar_ideias(dados_usuario):
    prompt = criar_prompt(dados_usuario)

    try:
        response = get_groq_completions(prompt)
        return response.strip() if response else None
    except Exception as e:
        st.error(f"Erro ao tentar gerar plano de trabalho: {e}")
        return None

# Função para criar o prompt com base nos dados do usuário
def criar_prompt(dados_usuario):
    metodologia = dados_usuario.get('metodologia')

    if metodologia == "Engenharia":
        prompt_template = """
        Crie um plano de trabalho para um projeto de pesquisa para uma feira de ciência que tem como título {titulo}. O objetivo do projeto é {objetivo}. Na execução do projeto será utilizado os seguintes materiais: {materiais}. A proposta que busco deve conter os seguintes elementos:\n     
     
        1.Propósito de Trabalho:\n
        Nesta seção, explicarei a razão de ser do projeto, isto é, qual problema ou desafio específico pretendo abordar. Além disso, ressaltarei os benefícios desta iniciativa e as suas possíveis contribuições.\n

        2.Características Físicas e Funcionais:\n
        Detalharei as características físicas e funcionais do projeto, explicando como ele será construído e como suas partes interagem para solucionar o problema proposto.\n

        3.Restrições/Limitações:\n
        Abordarei quaisquer restrições ou limitações que possam afetar o desenvolvimento ou a implementação do projeto. Isso pode incluir restrições orçamentárias, de tempo, de recursos, entre outras.\n

        4.Avaliação:\n
        Explicarei os critérios de avaliação que serão usados para medir o sucesso do projeto. Isso pode envolver testes, análises comparativas, pesquisas de satisfação, entre outros métodos de avaliação.\n

        5.Cronograma:\n
        Criarei um cronograma detalhado em 4 meses, dividindo o projeto em etapas mensais, para garantir um desenvolvimento organizado e dentro do prazo estabelecido.\n

        6.Bibliografia:\n
        Incluirei uma lista de pelo menos três (3) fontes utilizadas para embasar o projeto. Isso engloba livros, artigos científicos, sites e outras referências relevantes que inspiram para sua concepção.\n
        """
    elif metodologia == "Científica":
        prompt_template = """
        Crie um plano de trabalho para um projeto de pesquisa para uma feira de ciência que tem como título {titulo}. O objetivo do projeto é {objetivo}. Na execução do projeto será utilizado os seguintes materiais: {materiais}. A proposta que busco deve conter os seguintes elementos:\n
       
        1.Propósito de trabalho:\n
        Explique o objetivo principal do projeto, ou seja, qual a pergunta ou problema que pretendo investigar. É importante destacar o significado e o impacto do projeto, bem como o que espero alcançar ao final da pesquisa.\n

        2.Hipótese:\n
        Apresente uma suposição inicial sobre os resultados da pesquisa. A hipótese é uma afirmativa que procura responder o problema de pesquisa com base em conhecimentos prévios e pesquisas sobre o assunto.\n

        3.Método:\n 
        Descreva o método que pretende utilizar para conduzir a pesquisa. Isso inclui os procedimentos que serão seguidos e como os dados serão coletados.\n

        4.Materiais:\n
        Liste todos os materiais e equipamentos necessários para realizar o projeto. É importante ser específico e detalhado para que outros possam reproduzir o experimento, se necessário.\n

        5.Análise de dados:\n
        Explique como os dados coletados serão analisados. Isso pode envolver o uso de gráficos, estatísticas ou outras ferramentas relevantes para interpretar os resultados.\n

        6.Cronograma:\n
        Crie um cronograma detalhado em 4 meses, dividindo o projeto em etapas mensais, para garantir um desenvolvimento organizado e dentro do prazo estabelecido.\n

        7.Bibliografia:\n
        Inclua uma lista de pelo menos três (3) fontes utilizadas para embasar o projeto. Isso engloba livros, artigos científicos, sites e outras referências relevantes que inspiram para sua concepção.\n
        """

    return prompt_template.format(
        titulo=dados_usuario['titulo'],
        objetivo=dados_usuario['objetivo'],
        materiais=dados_usuario['materiais']
    )

# Configuração da aplicação Streamlit
st.title("Crie planos de trabalho incríveis com o Lampejo, seu assistente virtual!")

# Centralizando a imagem usando colunas
col1, col2 = st.columns(2)

with col1:
    st.write("")

with col2:
    st.write("")

st.write("""
Com o Lampejo, você tem um assistente inteligente pronto para ajudar na criação de Planos de Trabalho para seus projetos de pesquisa!
""")

st.write("""
Para que o Lampejo possa te oferecer as melhores sugestões, é fundamental que você responda a todas as perguntas.
""")

# Coletando informações do usuário
titulo = st.text_input("Qual é o título do seu projeto?", key="titulo")
objetivo = st.text_area("Qual é o objetivo do seu projeto?", key="objetivo")
materiais = st.text_area("Quais materiais você vai utilizar?", key="materiais")

metodologia = st.selectbox("Qual metodologia você pretende utilizar para o seu projeto?", ["", "Científica", "Engenharia"], key="metodologia")

# Dados do usuário para o prompt
dados_usuario = {
    'titulo': titulo,
    'objetivo': objetivo,
    'materiais': materiais,
    'metodologia': metodologia
}

# Gerar ideias de projetos
if st.button("Gerar Plano de Trabalho"):
    if not titulo or not objetivo or not materiais or not metodologia:
        st.error("Por favor, preencha todos os campos.")
    else:
        st.write("Aqui está um Plano de Trabalho para você:")
        response = gerar_ideias(dados_usuario)
        if response:
            st.write(response)

