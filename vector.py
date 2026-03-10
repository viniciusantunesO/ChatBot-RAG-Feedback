# vector.py
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Carrega dataset
df = pd.read_csv("./data/pokemon.csv")

# Garantir que a URL do Ollama esteja correta
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
    base_url=OLLAMA_HOST  # Use sempre base_url correto
)

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

documents = []
ids = []

if add_documents:
    for i, row in df.iterrows():
        texto = " ".join(str(x) for x in row.values)
        document = Document(
            page_content=texto,
            metadata={"row": i},
            id=str(i)
        )
        documents.append(document)
        ids.append(str(i))

vector_store = Chroma(
    collection_name="pokemon",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Cria retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)