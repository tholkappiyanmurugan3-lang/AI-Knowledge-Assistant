from src.pdf_loader import load_pdf
from src.text_splitter import split_text
from src.vector_store import create_vector_store

text = load_pdf("data/sample.pdf")

chunks = split_text(text)

print("Chunks Created:", len(chunks))

vector_db = create_vector_store(chunks)

print("FAISS Database Created Successfully")