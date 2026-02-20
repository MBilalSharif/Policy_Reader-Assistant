import streamlit as st
from rag.loader import load_and_chunk_pdf
from rag.vectorstore import create_vectorstore, load_vectorstore, get_retriever
from rag.llm import get_llm, get_prompt
from rag.chain import build_chain
from rag.config import VECTORSTORE_DIR
import os

st.set_page_config(page_title="LinkedIn Policy RAG", page_icon="📄")
st.title("📄 LinkedIn Policy Assistant")

@st.cache_resource
def initialize():
    # Load or create vectorstore
    if os.path.exists(VECTORSTORE_DIR):
        vectorstore = load_vectorstore()
    else:
        chunks = load_and_chunk_pdf()
        vectorstore = create_vectorstore(chunks)

    retriever = get_retriever(vectorstore)
    llm = get_llm()
    prompt = get_prompt()
    chain = build_chain(retriever, prompt, llm)
    return chain

chain = initialize()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("Ask about LinkedIn Policy..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke(user_input)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})