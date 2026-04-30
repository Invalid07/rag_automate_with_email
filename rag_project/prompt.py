from langchain_core.prompts import ChatPromptTemplate

# ─────────────────────────────────────────
# Default Auto Query
# ─────────────────────────────────────────
DEFAULT_QUERY = "Give a summary of the issues mentioned in this file and also provide solutions for each issue."

# ─────────────────────────────────────────
# RAG Prompt Template
# ─────────────────────────────────────────
rag_prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the context below.
with proper formatting and bullet points if needed.
give proper space between each solution:
                                        
in  proper mail formate with subject and greeting and closing:
                                              
at below write that this ai generated mail and also write the date and time of generation:
Context: {context}

Question: {question}
""")
