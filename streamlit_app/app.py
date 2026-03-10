import streamlit as st
import requests
import json
import re
from vector import retriever
import os

# Configuração inicial da página para aproveitar melhor o espaço da tela
st.set_page_config(page_title="Elephant ChatBot", layout="wide")

# Endpoint do Ollama - configurado para rodar tanto local quanto via Docker
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434/api/generate"
)
MODELO = "llama3"

# Template do Prompt do Sistema: aqui é onde a "mágica" acontece. 
# Deixei espaços reservados para injetar feedbacks e perguntas dinamicamente.
SYSTEM_PROMPT = """
Você é o Elephant, um assistente inteligente criado para ajudar usuários respondendo perguntas de forma clara, útil e confiável.

Seu objetivo é fornecer respostas precisas, bem explicadas e fáceis de entender.

REGRAS DE COMPORTAMENTO:
- Sempre responda de forma educada, clara e objetiva.
- Caso não saiba a resposta, diga honestamente que não possui informação suficiente.
- Utilize ferramentas externas disponíveis quando necessário.
- Utilize o contexto recuperado da vector store quando ele estiver disponível.

APRENDIZADO COM FEEDBACK:
{feedback_improvements}

PERGUNTA DO USUÁRIO:
{pergunta}
"""

# --- GERENCIAMENTO DE ESTADO (Session State) ---
# Essencial no Streamlit para evitar que os dados sumam a cada atualização de página
if "messages" not in st.session_state:
    st.session_state.messages = []  # Armazena o histórico da conversa
if "feedback_history" not in st.session_state:
    st.session_state.feedback_history = []  # Logs de feedbacks enviados
if "improvements" not in st.session_state:
    st.session_state.improvements = "" # String que acumula as melhorias de prompt

# --- INTEGRAÇÕES COM APIs EXTERNAS ---

def buscar_cachorro():
    """Consome a Dog CEO API para trazer uma imagem aleatória se o usuário pedir."""
    url = "https://dog.ceo/api/breeds/image/random"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()["message"]
    return None

def extrair_cep(texto):
    """Usa Regex para identificar padrões de CEP em mensagens de texto."""
    match = re.search(r"\d{5}-?\d{3}", texto)
    return match.group() if match else None

def buscar_cep(cep):
    """Integração com ViaCEP para enriquecer a resposta com dados de localização."""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        return None if "erro" in dados else dados
    return None

# --- LÓGICA PRINCIPAL DE IA ---

def perguntar(msg):
    """
    Orquestra a inteligência: combina contexto de APIs, busca vetorial 
    e feedbacks dinâmicos para gerar a resposta final via Ollama.
    """
    contexto_api = ""
    
    # Verifica se há necessidade de busca de CEP
    cep = extrair_cep(msg)
    if cep:
        dados = buscar_cep(cep)
        if dados:
            contexto_api = f"Rua: {dados['logradouro']}, Bairro: {dados['bairro']}, Cidade: {dados['localidade']} - {dados['uf']}"

    # Resposta especial para amantes de cachorros (Easter Egg)
    if "cachorro" in msg.lower():
        imagem = buscar_cachorro()
        if imagem:
            st.image(imagem)
            return "Aqui está um cachorro aleatório para alegrar seu dia! 🐶"

    # Busca semântica no banco de dados vetorial (RAG)
    docs = retriever.invoke(msg)
    contexto_vetorial = "\n".join([doc.page_content for doc in docs])

    # Montagem do Prompt Dinâmico: Aqui aplicamos os feedbacks que o usuário enviou na outra aba
    prompt_formatado = SYSTEM_PROMPT.format(
        feedback_improvements=st.session_state.improvements,
        pergunta=msg
    )

    # Payload final para o LLM
    prompt_final = f"{prompt_formatado}\n\nCONTEXTO API: {contexto_api}\nCONTEXTO VETORIAL: {contexto_vetorial}"
    
    response = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt_final, "stream": False})
    return response.json()['response']

# --- INTERFACE DO USUÁRIO (Streamlit) ---

st.title("🐘 Elephant AI - Assistente Inteligente")

# Organização em abas para separar a conversa da área de configuração (requisito de UX)
tab1, tab2 = st.tabs(["💬 Chat", "⚙️ Ajustes de Comportamento"])

with tab1:
    st.subheader("Conversa em tempo real")
    
    # Renderiza o histórico de mensagens de forma amigável
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Captura a interação do usuário
    if pergunta := st.chat_input("Como posso te ajudar hoje?", key="chat_principal"):
        st.session_state.messages.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.write(pergunta)
            
        with st.spinner("O Elephant está processando sua resposta..."):
            resposta = perguntar(pergunta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            with st.chat_message("assistant"):
                st.write(resposta)

with tab2:
    st.header("Sistema de Melhoria Contínua")
    st.write("Aqui você pode ajustar como o agente se comporta enviando feedbacks.")
    
    # Expander para transparência: o usuário vê exatamente o que a IA está lendo
    with st.expander("🔍 Inspecionar Prompt Atual"):
        st.code(SYSTEM_PROMPT.format(
            feedback_improvements=st.session_state.improvements,
            pergunta="..."
        ))

    # Formulário para envio de melhorias de comportamento
    with st.form("form_feedback"):
        sugestao = st.text_area("Descreva como a IA deve melhorar (ex: 'seja mais direto')")
        if st.form_submit_button("Atualizar Comportamento"):
            if sugestao:
                st.session_state.feedback_history.append(sugestao)
                # Adiciona a nova instrução à memória de melhorias
                st.session_state.improvements += f"\n- {sugestao}"
                st.success("Feedback processado! O agente agora seguirá estas novas instruções.")

    # Lista de histórico para auditoria de feedbacks
    st.subheader("📜 Histórico de Versões do Agente")
    for i, fb in enumerate(st.session_state.feedback_history):
        st.info(f"Ajuste #{i+1}: {fb}")

