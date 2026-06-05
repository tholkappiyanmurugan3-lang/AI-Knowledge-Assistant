from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


DB_PATH = "vector_store"


def get_embeddings():
    """
    Load embedding model
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store(chunks):
    """
    Create and save FAISS vector database
    """

    embeddings = get_embeddings()

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    vector_store.save_local(DB_PATH)

    return vector_store


def load_vector_store():
    """
    Load existing FAISS vector database
    """

    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store