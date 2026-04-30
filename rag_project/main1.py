import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from gmail_tool import send_email_smtp

import tkinter as tk
from tkinter import filedialog

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# ─────────────────────────────────────────
# Step 1: File Picker
# ─────────────────────────────────────────
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select a text file",
    filetypes=[("Text files", "*.txt")]
)

if not file_path:
    print("❌ No file selected")
    exit()

print(f"📂 Selected file: {file_path}")

# ─────────────────────────────────────────
# Step 2: Load file
# ─────────────────────────────────────────
loader = TextLoader(file_path, encoding="utf-8")
documents = loader.load()

# ─────────────────────────────────────────
# Step 3: Split into chunks
# ─────────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs = splitter.split_documents(documents)
print(f"📄 Total chunks: {len(docs)}")

# ─────────────────────────────────────────
# Step 4: Embeddings (Free - HuggingFace)
# ─────────────────────────────────────────
print("⏳ Loading embeddings model...")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ─────────────────────────────────────────
# Step 5: Vector DB (Chroma)
# ─────────────────────────────────────────
vectordb = Chroma.from_documents(docs, embeddings)
retriever = vectordb.as_retriever()

# ─────────────────────────────────────────
# Step 6: LLM (Groq - Free)
# ─────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# ─────────────────────────────────────────
# Step 7: Prompt Template
# ─────────────────────────────────────────
# prompt = ChatPromptTemplate.from_template("""
# Answer the question based only on the context below.
# with proper formatting and bullet points if needed.
# give proper space between each solution:

# Context: {context}

# Question: {question}
# """)
from prompt import rag_prompt as prompt , DEFAULT_QUERY

# ─────────────────────────────────────────
# Step 8: RAG Chain
# ─────────────────────────────────────────
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ─────────────────────────────────────────
# Step 9: Auto Query (no input needed)
# ─────────────────────────────────────────
query = "Give a summary of the issues mentioned in this file and also provide solutions for each issue."
print(f"\n💬 Query: {query}")

result = rag_chain.invoke(query)
print("\n📌 Answer:\n", result)

# ─────────────────────────────────────────
# Step 10: Email Option with CC and BCC
# ─────────────────────────────────────────
choice = input("\n📧 Send answer via email? (yes/no): ")

if choice.lower() == "yes":
    to_email = input("Enter recipient email (To): ")

    cc_email = input("Enter CC email (press Enter to skip): ").strip()
    bcc_email = input("Enter BCC email (press Enter to skip): ").strip()

    send_email_smtp(
        to=to_email,
        subject="sapphireinfotech - Issues & Solutions",
        message=result,
        cc=cc_email,
        bcc=bcc_email
    )
    print("✅ Email sent successfully!")
else:
    print("❌ Email skipped")