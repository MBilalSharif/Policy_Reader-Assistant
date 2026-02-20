from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from rag.config import EMBEDDING_MODEL, VECTORSTORE_DIR

def get_embeddings():
    return HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL)

def create_vectorstore(chunks):
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )
    print("Vector DB Created")
    return vectorstore

def load_vectorstore():
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings
    )

def get_retriever(vectorstore):
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )