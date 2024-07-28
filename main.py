import os
import streamlit as st
from groq import Groq

# Função para obter as respostas do Groq
def get_groq_completions(user_content):
    client = Groq(
        api_key="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",
    )

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": "You are a YouTube expert creator who likes to write engaging titles for a keyword. \nYou will provide 10 attention-grabbing YouTube titles on keywords specified by the user."
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

# Função para gerar ideias de projetos de feira de ciências
def gerar_ideias(dados_usuario):
    prompt = criar_prompt(dados_usuario)

    try:
        response = get_groq_completions(prompt)
        return response.strip() if response else None
    except Exception as e:
        st.error(f"Erro ao tentar gerar ideias: {e}")
        return None

# Função para criar o prompt com base nos dados do usuário
def criar_prompt(dados_usuario):
    metodologia = dados_usuario.get('metodologia')

    if metodologia == "Engenharia":
        prompt_template = """
        Crie um plano de trabalho para um projeto de pesquisa para uma feira de ciência que tem como título {titulo}. O objetivo do projeto é {objetivo}. Na execução do projeto será utilizado os seguintes materiais: {materiais}. A proposta que busco deve conter os seguintes elementos:

        #Propósito de Trabalho : Nesta seção, explicarei a razão de ser do projeto, isto é, qual problema ou desafio específico pretendo abordar. Além disso, ressaltarei os benefícios desta iniciativa e as suas possíveis contribuições.

        #Características Físicas e Funcionais : Detalharei as características físicas e funcionais do projeto, explicando como ele será construído e como suas partes interagem para solucionar o problema proposto.

        #Restrições/Limitações : Abordarei quaisquer restrições ou limitações que possam afetar o desenvolvimento ou a implementação do projeto. Isso pode incluir restrições orçamentárias, de tempo, de recursos, entre outras.

        #Avaliação : Explicarei os critérios de avaliação que serão usados para medir o sucesso do projeto. Isso pode envolver testes, análises comparativas, pesquisas de satisfação, entre outros métodos de avaliação.

        #Cronograma : Criarei um cronograma detalhado em 4 meses, dividindo o projeto em etapas mensais, para garantir um desenvolvimento organizado e dentro do prazo estabelecido.

        #Bibliografia : Incluirei uma lista de pelo menos três (3) fontes utilizadas para embasar o projeto. Isso engloba livros, artigos científicos, sites e outras referências relevantes que inspiram para sua concepção.
        """
    elif metodologia == "Científica":
        prompt_template = """
        Crie um plano de trabalho para um projeto de pesquisa para uma feira de ciência que tem como título {titulo}. O objetivo do projeto é {objetivo}. Na execução do projeto será utilizado os seguintes materiais: {materiais}. A proposta que busco deve conter os seguintes elementos:

        #1) Título
        Escolha um título que reflita claramente o escopo do projeto.

        #2) Propósito de trabalho
        Explique o objetivo principal do projeto, ou seja, qual a pergunta ou problema que pretendo investigar. É importante destacar o significado e o impacto do projeto, bem como o que espero alcançar ao final da pesquisa.

        #3) Hipótese
        Apresente uma suposição inicial sobre os resultados da pesquisa. A hipótese é uma afirmativa que procura responder o problema de pesquisa com base em conhecimentos prévios e pesquisas sobre o assunto.

        #4) Método 
        Descreva o método que pretende utilizar para conduzir a pesquisa. Isso inclui os procedimentos que serão seguidos e como os dados serão coletados.

        #5) Materiais
        Liste todos os materiais e equipamentos necessários para realizar o projeto. É importante ser específico e detalhado para que outros possam reproduzir o experimento, se necessário.

        #6) Análise de dados
        Explique como os dados coletados serão analisados. Isso pode envolver o uso de gráficos, estatísticas ou outras ferramentas relevantes para interpretar os resultados.

        #7) Cronograma
        Crie um cronograma detalhado em 4 meses, dividindo o projeto em etapas mensais, para garantir um desenvolvimento organizado e dentro do prazo estabelecido.

        #8) Bibliografia
        Inclua uma lista de pelo menos três (3) fontes utilizadas para embasar o projeto. Isso engloba livros, artigos científicos, sites e outras referências relevantes que inspiram para sua concepção.
        """

    return prompt_template.format(
        titulo=dados_usuario['titulo'],
        objetivo=dados_usuario['objetivo'],
        materiais=dados_usuario['materiais']
    )

# Configuração da aplicação Streamlit
st.title("Tenha ideias incríveis de projetos com o Faísca, seu assistente virtual!")

# Centralizando a imagem usando colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    st.image("C:/Users/IFmaker02/PycharmProjects/streamilt/faisca.png", use_column_width=True)

with col3:
    st.write("")

st.write("""
Faísca é um chatbot de inteligência artificial feito sob medida para alunos da educação básica como você. Ele não é apenas um assistente; é uma fonte de inspiração que irá acender sua criatividade e ajudá-lo a gerar ideias para seus projetos.
""")

st.write("""
Para que o Faísca possa te oferecer as melhores sugestões, é fundamental que você responda a todas as perguntas.
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
if st.button("Gerar Ideias de Projetos"):
    if not titulo or not objetivo or not materiais or not metodologia:
        st.error("Por favor, preencha todos os campos.")
    else:
        st.write("Aqui estão algumas ideias de projetos para você:")
        response = gerar_ideias(dados_usuario)
        if response:
            st.write(response)

