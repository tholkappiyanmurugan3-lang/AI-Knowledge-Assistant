import streamlit as st
import tempfile

from src.pdf_loader import load_pdf
from src.text_splitter import split_text
from src.retriever import retrieve_context
from src.chatbot import get_llm
from src.vector_store import create_vector_store, load_vector_store

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_db_ready" not in st.session_state:
    st.session_state.vector_db_ready = False

if "pdf_count" not in st.session_state:
    st.session_state.pdf_count = 0

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# ================= PREMIUM CSS =================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #334155
    );
}

/* Main Container */
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0B1120;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* File Uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #3B82F6;
    border-radius: 18px;
    padding: 15px;
    background: rgba(255,255,255,0.04);
}

/* Buttons */
.stButton button {
    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    );
    color: white;
    border-radius: 14px;
}

/* Download Button */
.stDownloadButton button {
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
    color: white;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    padding: 15px;
}
/* Chat Input Box */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(10px);
    border-radius: 25px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
h1 {
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    to {
        text-shadow: 0 0 30px rgba(255,255,255,0.8);
    }
}
/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a,
        #111827,
        #1e293b
    );
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar Title */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
    font-weight: 700;
}

/* File Uploader Container */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(12px);
    border: 2px dashed #60a5fa !important;
    border-radius: 20px !important;
    padding: 20px !important;
}

/* Upload Button */
[data-testid="stFileUploader"] button {
    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* Upload Text */
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] label {
    color: #e2e8f0 !important;
}

/* Drag & Drop Area */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 16px !important;
}
/* Statistics Cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 10px;
    backdrop-filter: blur(10px);
}

/* Metric Labels */
[data-testid="metric-container"] label {
    color: #cbd5e1 !important;
    font-size: 14px !important;
}

/* Metric Values */
[data-testid="metric-container"] div {
    color: white !important;
    font-weight: 700 !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* Sidebar Text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
}

[data-testid="stFileUploader"] {
    box-shadow:
        0 0 20px rgba(59,130,246,0.3),
        0 0 40px rgba(139,92,246,0.2);
}/* Inner Upload Area */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 2px dashed #60a5fa !important;
    border-radius: 18px !important;
    padding: 25px !important;
}

/* Upload Button */
[data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* Upload Text */
[data-testid="stFileUploaderDropzone"] * {
    color: #e2e8f0 !important;
}
[data-testid="metric-container"] {
    text-align:center;
}

[data-testid="metric-container"] > div {
    font-size: 28px !important;
    font-weight: 700 !important;
}
/* Chat Input Box */
[data-testid="stChatInput"] {
    background: linear-gradient(
        90deg,
        #3B82F6,
        #06B6D4
    ) !important;
    border-radius: 20px !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    padding: 10px !important;
}

/* Hide Streamlit Branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)
# ================= HEADER =================
st.markdown("""
<div style="text-align:center;padding:20px;">

<h1 style="
font-size:4rem;
font-weight:900;
background: linear-gradient(
90deg,
#60a5fa,
#818cf8,
#c084fc
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
">
🤖 AI Knowledge Assistant
</h1>

<p style="
font-size:1.2rem;
color:#cbd5e1;">
✨ Your Personal PDF Research Assistant
</p>

</div>
""", unsafe_allow_html=True)

# ================= WELCOME CARD =================
if not st.session_state.get("vector_db_ready", False):
    st.markdown("""
    <div style="
        text-align:center;
        padding:60px;
        background:rgba(255,255,255,0.05);
        border-radius:20px;
        margin-top:30px;">
        <h2>📚 Upload PDFs to Get Started</h2>
        <p>Ask questions, summarize documents, and search knowledge instantly.</p>
    </div>
    """, unsafe_allow_html=True)
# ================= SIDEBAR =================
with st.sidebar:

    st.markdown("""
    ## 📚 AI Knowledge Assistant

    Powered by Gemini AI
    """)

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.markdown("### 📄 Uploaded Documents")

        for file in uploaded_files:
            st.caption(f"• {file.name}")

    process = st.button(
        "🚀 Process PDFs",
        use_container_width=True
    )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### 📊 Statistics")

    st.metric(
        "PDFs",
        st.session_state.get("pdf_count", 0)
    )

    st.metric(
        "Chunks",
        st.session_state.get("chunk_count", 0)
    )

    st.metric(
        "Status",
        "Ready" if st.session_state.vector_db_ready else "Not Ready"
    )

    st.divider()

    st.caption("Built with Streamlit + Gemini + FAISS")

# ================= PDF PROCESSING =================
if process and uploaded_files:

    try:

        all_text = ""

        with st.spinner("Processing PDFs..."):

            for file in uploaded_files:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(file.read())
                    tmp.flush()

                    text = load_pdf(tmp.name)
                    all_text += text

            chunks = split_text(all_text)

            create_vector_store(chunks)
            st.session_state.pdf_count = len(uploaded_files)
            st.session_state.chunk_count = len(chunks)


        st.session_state.vector_db_ready = True

        st.success("✅ Knowledge Base Created Successfully!")
        chunks = split_text(all_text)


        
        # Generate AI Questions
# Generate AI Questions
        try:
            llm = get_llm()

            sample_context = "\n".join(
                [str(chunk) for chunk in chunks[:5]]
            )

            question_prompt = f"""
            Based on the document content below, generate 4 useful questions
            a user might want to ask.

            Return ONLY the questions.
            One question per line.

            Document:
            {sample_context}
            """

            response = llm.invoke(question_prompt)
            response_text = str(response.content)
            suggested_questions = [
                q.strip("-• ").strip()
                for q in response_text.split("\n")
                if q.strip()
            ][:4]

            st.session_state["suggested_questions"] = suggested_questions

        except Exception:
            st.session_state["suggested_questions"] = [
                "Summarize the document",
                "What are the key findings?",
                "What is the main objective?",
                "What conclusions are given?"
            ]

        # Metrics Section
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📄 PDFs",
                len(uploaded_files)
            )

        with col2:
            st.metric(
                "🧩 Chunks",
                len(chunks)
            )

        with col3:
            st.metric(
                "🤖 Status",
                "Ready"
            )

    except Exception as e:
        st.error(f"PDF Processing Error: {e}")
# ================= LOAD VECTOR DB =================
vector_db = None

if st.session_state.vector_db_ready:

    try:
        vector_db = load_vector_store()

    except Exception as e:
        st.error(
            f"Error Loading Vector Store: {e}"
        )

# ================= CHAT HISTORY =================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT INPUT =================
query = st.chat_input(
    "Ask a question from your PDFs..."
)

if "suggested_query" in st.session_state:
    query = st.session_state["suggested_query"]
    del st.session_state["suggested_query"]

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    if vector_db is None:

        with st.chat_message("assistant"):
            st.warning(
                "⚠️ Please upload and process PDFs first."
            )

    else:

        try:

            context, docs = retrieve_context(
                vector_db,
                query
            )

            llm = get_llm()

            prompt = f"""
You are an expert document question answering assistant.

Use ONLY the information present in the context.

Instructions:
- Read the complete context carefully.
- Give a direct and accurate answer.
- If the answer spans multiple sections, combine them.
- Explain the answer clearly.
- Do not hallucinate or invent information.
- If the answer is not present, say:
  "I could not find that information in the uploaded documents."

Context:
{context}

Question:
{query}

Answer:
"""

            with st.spinner("Thinking..."):

                response = llm.invoke(prompt)
                answer = response.content
            
            with st.expander("Retrieved Context"):
                st.write(context)

            with st.chat_message("assistant"):

                st.markdown(answer)

                if docs:
                    st.markdown("### 📄 Sources")
                    for i, doc in enumerate(docs):
                        with st.expander(f"📄 Source {i+1}"):
                            st.write(doc.page_content)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:
            st.error(f"LLM Error: {e}")

# ================= DOWNLOAD CHAT ================= #
chat_text = ""

for msg in st.session_state.messages:

    chat_text += (
        f"{msg['role']}:\n"
        f"{msg['content']}\n\n"
    )

st.download_button(
    "📥 Download Chat",
    chat_text,
    file_name="chat_history.txt",
    mime="text/plain",
    use_container_width=True
)
