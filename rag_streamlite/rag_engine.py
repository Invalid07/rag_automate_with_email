import os
import tempfile

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from prompt import rag_prompt


# ─────────────────────────────────────────
# Load & Split Document
# ─────────────────────────────────────────
def load_and_split(file_bytes: bytes, chunk_size: int = 500, chunk_overlap: int = 50):
    """Save uploaded bytes to a temp file, load and split into chunks."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    loader = TextLoader(tmp_path, encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    docs = splitter.split_documents(documents)

    os.unlink(tmp_path)
    return docs


# ─────────────────────────────────────────
# Build Vector Store
# ─────────────────────────────────────────
def build_vectorstore(docs):
    """Create ChromaDB vector store with HuggingFace embeddings."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(docs, embeddings)
    return vectordb.as_retriever()


# ─────────────────────────────────────────
# Build RAG Chain
# ─────────────────────────────────────────
def build_rag_chain(retriever, groq_api_key: str, temperature: float = 0.4):
    """Build the full RAG chain using Groq LLM."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=groq_api_key,
        temperature=temperature
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


# ─────────────────────────────────────────
# Run Full Pipeline
# ─────────────────────────────────────────
def run_pipeline(file_bytes: bytes, query: str, groq_api_key: str,
                 temperature: float = 0.4, chunk_size: int = 500, chunk_overlap: int = 50):
    """End-to-end RAG pipeline: file → answer string."""
    docs = load_and_split(file_bytes, chunk_size, chunk_overlap)
    retriever = build_vectorstore(docs)
    chain = build_rag_chain(retriever, groq_api_key, temperature)
    result = chain.invoke(query)
    return result, len(docs)
