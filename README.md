# 🐘 Elephant AI - Chatbot com Feedback Inteligente

## 📝 Descrição do Projeto
O **Elephant AI** é uma solução de chatbot desenvolvida para demonstrar a implementação de um fluxo de **RAG (Retrieval-Augmented Generation)** com um sistema de **feedback em tempo real**. 

O projeto foca na orquestração de um agente de IA que utiliza uma base de dados vetorial para contexto, consome APIs externas e, o mais importante, **aprende e adapta seu comportamento** dinamicamente com base nas sugestões enviadas pelo usuário durante o uso.

---

## ⚠️ Pré-requisitos Importantes
* **Ollama instalado:** O projeto utiliza o Ollama como backend de IA. Baixe em [ollama.com](https://ollama.com).
* **Modelo Llama3:** Após instalar o Ollama, execute o comando abaixo no seu terminal para baixar o modelo usado no projeto:
### Modelo de Linguagem (LLM) - Responsável pelas respostas do chat
ollama pull llama3

### Modelo de Embedding - Essencial para o funcionamento da busca vetorial (RAG)
ollama pull mxbai-embed-large

---

## 🚀 Como Executar o Projeto

### 🐳 Via Docker (Recomendado)
Este projeto está totalmente dockerizado para garantir que o ambiente de execução seja idêntico em qualquer máquina.

1.  **Certifique-se de ter o Docker instalado.**
2.  **No terminal, execute o comando:**
    ```bash
    docker-compose up --build
    ```
3.  **Acesse a aplicação em:** `http://localhost:8501`

### 🐍 Execução Local
1.  Crie um ambiente virtual: `python -m venv venv`
2.  Instale as dependências: `pip install -r requirements.txt`
3.  Execute: `streamlit run app.py`

---

## 🛠️ Funcionalidades e Arquitetura 

O sistema foi organizado em duas áreas principais, conforme exigido pelos requisitos:

### 1. Área de Chat (Interface do Agente) 
* **Histórico Visível:** Implementado via `st.session_state` para garantir que as mensagens não se percam entre interações.
* **Interface Interativa:** Campo de entrada otimizado para perguntas e respostas rápidas.

### 2. Sistema de Feedback e Melhoria 
* **Captura de Feedback:** O usuário pode enviar sugestões de melhoria (ex: "seja mais conciso").
* **Atualização de Prompt:** O sistema processa o feedback e o injeta no `SYSTEM_PROMPT` do agente instantaneamente.
* **Versão e Logs:** É possível visualizar o prompt atual "sob o capô" e o histórico de todas as alterações feitas.

### 3. Ferramentas e Integrações (Tools) 
O Elephant utiliza integrações externas para enriquecer suas respostas:
* **ViaCEP API:** Consulta automática de endereços ao identificar um CEP na conversa (certifique-se de que na hora de digitar o cep, ter espaço entre os primeiros e ultimos numeros. Ex: "Qual cidade do cep 03247046 ?").
* **Dog API:** Ferramenta lúdica para exibição de imagens aleatórias de pets (para aparecer a imagem, deve mencionar a palavra "cachorro").
* **Vector Store (ChromaDB):** Base de dados para recuperação de documentos e contexto do dataset (foi usado dados sobre pokemon).

---

## 🔌 Documentação das APIs Utilizadas 

| API | Finalidade | Endpoint |
| :--- | :--- | :--- |
| **ViaCEP** | Busca de endereços brasileiros | `https://viacep.com.br/ws/{cep}/json/` |
| **Dog API** | Imagens aleatórias de cães | `https://dog.ceo/api/breeds/image/random` |
| **Ollama/Gemini** | Orquestração do Modelo de Linguagem | Configurado via variável de ambiente `OLLAMA_URL` |

---

## 🏗️ Requisitos Técnicos Atendidos 
* **Python 3.9+** 
* **Interface:** Streamlit 
* **LLM:** Llama 3 (via Ollama) / Integração via API 
* **Containerização:** Docker e Docker Compose 
* **RAG:** Busca vetorial para contexto persistente 

---

## 💡 Exemplo de Uso
1.  **Chat:** "Qual é o endereço do CEP 01001-000 ?"
2.  **Feedback:** Vá na aba "Feedback", digite "Responda de forma mais amigável e use emojis" e clique em atualizar.
3.  **Resultado:** Nas próximas interações, o Elephant adotará automaticamente o novo tom sugerido.

---

