from langchain_core.documents import Document

def retrieve_context(vector_db, query):

    docs = vector_db.similarity_search(
        query,
        k=8
    )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return context, docs