
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pypdf import PdfReader 
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma


doc = 'LinkedIn_Policy'
print(f"Using document {doc}")



def clean_text(doc):

    # Split into lines first
    lines = doc.split("\n")

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Remove page number lines
        if re.search(r'Page\s*\d+', line, re.IGNORECASE):
            continue

        # Remove TOC style lines (ending with number)
        if re.search(r'\.{2,}\s*\d+$', line):
            continue

        # Remove lines that are mostly dots
        if re.search(r'^\.*\s*\d+\s*$', line):
            continue

        cleaned_lines.append(line)

    # Join back
    doc = "\n".join(cleaned_lines)

    # Now normalize whitespace
    doc = re.sub(r'\n+', '\n', doc)
    doc = re.sub(r'[ \t]+', ' ', doc)

    return doc.strip()





text_splitter = RecursiveCharacterTextSplitter(
chunk_size = 1000,
chunk_overlap = 200
)


reader = PdfReader(f"/data/{doc}.pdf")
pages = [page.extract_text() for page in reader.pages]

documents = []

for i, page_text in enumerate(pages):
    cleaned = clean_text(page_text)
    documents.append(
        Document(
            page_content=cleaned,
            metadata={"page": i+1}
        )
    )

chunks = text_splitter.split_documents(documents)
print(f"Number of chunks: {len(chunks)}")


embeddings = HuggingFaceBgeEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents = chunks,
    embedding = embeddings,
    persist_directory = "./doc_vectorstore"
)

print("Vectore DB Created")


retriever = vectorstore.as_retriever(search_type = "similarity" , search_kwargs={"k":5})
retriever.invoke("What is Privacy Policy")


import google.generativeai as genai
from getpass import getpass
from langchain_google_genai import ChatGoogleGenerativeAI

api_key = getpass("Paste your key:")
genai.configure(api_key=api_key)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_output_tokens=2000,
    google_api_key=api_key # Pass the API key explicitly
)

print("Gemini is good to go")

from langchain_core.prompts import PromptTemplate

prompt= PromptTemplate(
  
    template  = """

    You are a helpful assistant
    Answer only from the provided context
    If the context is insufficent, just say I don't know the answer                  

    {context}
    Question= {question}                   
    """,
    input_variables=['context', 'question']
)


question = "How LinkedIn create a healthy enviornemnt ?"
retrieved_docs= retriever.invoke(question)

context_text = "n\n".join(doc.page_content for doc in retrieved_docs)
print(context_text)

final_prompt = prompt.format(context = context_text  , question = question)

response = model(final_prompt)
print(response)

from langchain_core.runnables import RunnableLambda,RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def formatDocs(retrieved_docs):
  context_text = "n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

format_docs_runnable = RunnableLambda(formatDocs)


parallel_chain = RunnableParallel({
  'context': retriever | RunnableLambda(formatDocs),
  'question': RunnablePassthrough()
})

parser = StrOutputParser()

main_chain = parallel_chain | prompt | model | parser

response = main_chain.invoke(question)
print(response)