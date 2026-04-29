import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from gmail_tool import authenticate_gmail, send_email

import tkinter as tk
from tkinter import filedialog
load_dotenv()

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
loader = TextLoader(file_path)
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
# Step 4: Embeddings (OpenAI)
# ─────────────────────────────────────────
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# ─────────────────────────────────────────
# Step 5: Vector DB (Chroma)
# ─────────────────────────────────────────
vectordb = Chroma.from_documents(docs, embeddings)
retriever = vectordb.as_retriever()

# ─────────────────────────────────────────
# Step 6: LLM (OpenAI GPT-4o-mini)
# ─────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# ─────────────────────────────────────────
# Step 7: Prompt Template
# ─────────────────────────────────────────
prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the context below.

Context: {context}

Question: {question}
""")

# ─────────────────────────────────────────
# Step 8: RAG Chain (modern style)
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
# Step 9: Ask Question
# ─────────────────────────────────────────
query = "look at file and give solution  of each question present in file "
result = rag_chain.invoke(query)

print("\n📌 Answer:\n", result)

# ─────────────────────────────────────────
# Step 10: Email Option
# ─────────────────────────────────────────
choice = input("\n📧 Send answer via email? (yes/no): ")

if choice.lower() == "yes":
    to_email = input("Enter recipient email: ")
    service = authenticate_gmail()
    send_email(
        service,
        to_email,
        subject="RAG Answer",
        message=result
    )
    print("✅ Email sent successfully!")
else:
    print("❌ Email skipped")