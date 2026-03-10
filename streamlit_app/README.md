# 🐘 Elephant AI - Chatbot com Feedback Inteligente

## 📝 Descrição do Projeto
[cite_start]O **Elephant AI** é uma solução de chatbot desenvolvida para demonstrar a implementação de um fluxo de **RAG (Retrieval-Augmented Generation)** com um sistema de **feedback em tempo real**[cite: 4, 5]. 

[cite_start]O projeto foca na orquestração de um agente de IA que utiliza uma base de dados vetorial para contexto, consome APIs externas e, o mais importante, **aprende e adapta seu comportamento** dinamicamente com base nas sugestões enviadas pelo usuário durante o uso[cite: 26, 30].

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

### [cite_start]🐳 Via Docker (Recomendado) [cite: 66, 69]
Este projeto está totalmente dockerizado para garantir que o ambiente de execução seja idêntico em qualquer máquina.

1.  **Certifique-se de ter o Docker instalado.**
2.  **No terminal, execute o comando:**
    ```bash
    docker-compose up --build
    ```
3.  **Acesse a aplicação em:** `http://localhost:8501`

### 🐍 Execução Local
1.  Crie um ambiente virtual: `python -m venv venv`
2.  [cite_start]Instale as dependências[cite: 70]: `pip install -r requirements.txt`
3.  Execute: `streamlit run app.py`

---

## [cite_start]🛠️ Funcionalidades e Arquitetura [cite: 6, 18]

[cite_start]O sistema foi organizado em duas áreas principais, conforme exigido pelos requisitos[cite: 8, 35]:

### [cite_start]1. Área de Chat (Interface do Agente) [cite: 9]
* [cite_start]**Histórico Visível:** Implementado via `st.session_state` para garantir que as mensagens não se percam entre interações[cite: 11].
* [cite_start]**Interface Interativa:** Campo de entrada otimizado para perguntas e respostas rápidas[cite: 12].

### [cite_start]2. Sistema de Feedback e Melhoria [cite: 13, 26]
* [cite_start]**Captura de Feedback:** O usuário pode enviar sugestões de melhoria (ex: "seja mais conciso")[cite: 14, 15, 27].
* [cite_start]**Atualização de Prompt:** O sistema processa o feedback e o injeta no `SYSTEM_PROMPT` do agente instantaneamente[cite: 59, 60].
* [cite_start]**Versão e Logs:** É possível visualizar o prompt atual "sob o capô" e o histórico de todas as alterações feitas[cite: 16, 17, 31].

### [cite_start]3. Ferramentas e Integrações (Tools) [cite: 22, 43]
[cite_start]O Elephant utiliza integrações externas para enriquecer suas respostas[cite: 56]:
* [cite_start]**ViaCEP API:** Consulta automática de endereços ao identificar um CEP na conversa[cite: 23, 87].
* [cite_start]**Dog API:** Ferramenta lúdica para exibição de imagens aleatórias de pets[cite: 25, 86].
* [cite_start]**Vector Store (ChromaDB):** Base de dados para recuperação de documentos e contexto do dataset[cite: 21, 41, 55].

---

## [cite_start]🔌 Documentação das APIs Utilizadas [cite: 68]

| API | Finalidade | Endpoint |
| :--- | :--- | :--- |
| **ViaCEP** | Busca de endereços brasileiros | `https://viacep.com.br/ws/{cep}/json/` |
| **Dog API** | Imagens aleatórias de cães | `https://dog.ceo/api/breeds/image/random` |
| **Ollama/Gemini** | Orquestração do Modelo de Linguagem | Configurado via variável de ambiente `OLLAMA_URL` |

---

## [cite_start]🏗️ Requisitos Técnicos Atendidos [cite: 38]
* [cite_start]**Python 3.9+** [cite: 40]
* [cite_start]**Interface:** Streamlit [cite: 33]
* [cite_start]**LLM:** Llama 3 (via Ollama) / Integração via API [cite: 20, 42]
* [cite_start]**Containerização:** Docker e Docker Compose [cite: 44, 76]
* [cite_start]**RAG:** Busca vetorial para contexto persistente [cite: 55]

---

## 💡 Exemplo de Uso
1.  **Chat:** "Qual é o endereço do CEP 01001-000?"
2.  **Feedback:** Vá na aba "Feedback", digite "Responda de forma mais amigável e use emojis" e clique em atualizar.
3.  [cite_start]**Resultado:** Nas próximas interações, o Elephant adotará automaticamente o novo tom sugerido[cite: 60].

---
Desenvolvido como critério de avaliação para o processo seletivo de Estágio em Desenvolvimento.