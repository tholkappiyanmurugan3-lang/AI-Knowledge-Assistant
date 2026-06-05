from src.pdf_loader import load_pdf
from src.text_splitter import split_text
from src.vector_store import create_vector_store
from src.retriever import retrieve_context
from src.chatbot import get_llm

# Load PDF
text = load_pdf("data/sample.pdf")

# Split Text
chunks = split_text(text)

# Create FAISS DB
vector_db = create_vector_store(chunks)

# User Query
query = input("Ask a question: ")

# Retrieve Context
context = retrieve_context(
    vector_db,
    query
)

# Gemini Model
llm = get_llm()

prompt = f"""
Answer the question only from the given context.

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)

print("\nAnswer:")
print(response.content)