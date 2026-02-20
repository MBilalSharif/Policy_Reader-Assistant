from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pypdf import PdfReader
from rag.utils import clean_text
from rag.config import DOC_PATH

def load_and_chunk_pdf():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    reader = PdfReader(DOC_PATH)
    pages = [page.extract_text() for page in reader.pages]

    documents = []
    for i, page_text in enumerate(pages):
        cleaned = clean_text(page_text)
        documents.append(
            Document(
                page_content=cleaned,
                metadata={"page": i + 1}
            )
        )

    chunks = text_splitter.split_documents(documents)
    print(f"Number of chunks: {len(chunks)}")
    return chunks