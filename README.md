# AI Knowledge Assistant

An AI-powered Knowledge Assistant built using Retrieval-Augmented Generation (RAG) that allows users to ask questions about their documents and receive intelligent answers using OpenAI models.

---

## Features

✅ PDF Document Loading

✅ Text Chunking and Processing

✅ Vector Embedding Storage

✅ Semantic Search and Retrieval

✅ OpenAI-Powered Question Answering

✅ Retrieval-Augmented Generation (RAG)

---

## Architecture

```text
User
  │
  ▼
PDF Loader
  │
  ▼
Text Splitter
  │
  ▼
Vector Store
  │
  ▼
Retriever
  │
  ▼
OpenAI LLM
  │
  ▼
Answer
```

Architecture Diagram:

+--------+
|  User  |
+--------+
     |
     v
+----------------+
| User Question  |
+----------------+
     |
     v
+----------------+
|   Retriever    |
+----------------+
     |
     v
+----------------+
| Vector Store   |
+----------------+
     |
     v
+----------------+
| Relevant Chunks|
+----------------+
     |
     v
+----------------+
| OpenAI Model   |
+----------------+
     |
     v
+----------------+
| Final Answer   |
+----------------+

---

## Tech Stack

* Python
* OpenAI API
* LangChain
* Vector Database (FAISS / ChromaDB)
* Git & GitHub

---

## Project Structure

AI-Knowledge-Assistant/
│
├── assets/
│   ├── architecture.png
│   └── screenshot1.png
│
├── data/
│   └── sample.txt
│
├── src/
│   ├── chatbot.py
│   ├── pdf_loader.py
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
│
├── vector_store/
│
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/tholkappiyanmurugan3-lang/AI-Knowledge-Assistant.git
cd AI-Knowledge-Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

---

## Usage

1. Add PDF documents to the `data` folder.
2. Run the application.
3. Ask questions about the uploaded documents.
4. The retriever fetches relevant chunks.
5. OpenAI generates a context-aware answer.

---

## Sample Data

A sample document is included:

streamlit
langchain
langchain-community
langchain-text-splitters
faiss-cpu
sentence-transformers
langchain-google-genai
pypdf
python-dotenv

## Screenshot

Application Screenshot:

<img width="1918" height="1158" alt="Screenshot 2026-06-05 171649" src="https://github.com/user-attachments/assets/f35b89b1-f627-46f7-891b-1bd65651c732" />


---

## Future Improvements

* Streamlit Web Interface
* Multiple PDF Upload Support
* Chat History
* Conversation Memory
* Advanced Search Filters
* Source Citation Support

---

## Author

**Tholkappiyan Murugan**

GitHub: https://github.com/tholkappiyanmurugan3-lang

---

## License

This project is licensed under the MIT License.
