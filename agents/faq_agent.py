from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from utils.gemini import gemini_llm

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "data" / "faq.pdf"

db = None

def load_db():
    global db

    if not PDF_PATH.exists():
        raise FileNotFoundError(f"FAQ PDF not found at {PDF_PATH}")

    loader = PyPDFLoader(str(PDF_PATH))
    docs = loader.load()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(docs, embeddings)


def faq_agent(question: str) -> str:
    global db

    if db is None:
        load_db()

    docs = db.similarity_search(question, k=3)
    context = "\n".join(d.page_content for d in docs)

    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {question}
    """

    return gemini_llm(prompt)
