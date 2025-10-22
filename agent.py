################################
# agent.py
import os
from pathlib import Path
from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# USE Your OpenRouter API Key
OPENROUTER_KEY = "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"
os.environ["OPENAI_API_KEY"] = OPENROUTER_KEY  # Required for ChatOpenAI


# Global variables
vectorstore = None
qa_chain = None
embedding_model = None


# Initialize FAISS + LLM
def init_vectorstore():
    """
    Initialize FAISS vectorstore and QA chain.
    Must be called on startup or before first document.
    """
    global vectorstore, qa_chain, embedding_model

    # Initialize embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if Path("faiss.index").exists():
        vectorstore = FAISS.load_local("faiss.index", embedding_model, allow_dangerous_deserialization=True)
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                model="tngtech/deepseek-r1t2-chimera:free",
                temperature=0,
                openai_api_key=OPENROUTER_KEY,
                openai_api_base="https://openrouter.ai/api/v1",
            ),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
        )
    else:
        vectorstore = None
        qa_chain = None


# Add a document to FAISS
def add_document(title: str, content: str):
    """
    Add a new document to the FAISS vectorstore and save index.
    """
    global vectorstore, qa_chain, embedding_model

    if embedding_model is None:
        init_vectorstore()

    if vectorstore is None:
        # First document
        vectorstore = FAISS.from_texts([content], embedding=embedding_model, metadatas=[{"title": title}])
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                model="tngtech/deepseek-r1t2-chimera:free",
                temperature=0,
                openai_api_key=OPENROUTER_KEY,
                openai_api_base="https://openrouter.ai/api/v1",
            ),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
        )
    else:
        # Add to existing vectorstore
        vectorstore.add_texts([content], metadatas=[{"title": title}])

    # Save index locally
    vectorstore.save_local("faiss.index")


# Ask a question via RAG
def ask_question(query: str):
    """
    Query the QA chain. Returns a string answer.
    """
    global qa_chain, vectorstore

    if vectorstore is None or qa_chain is None:
        return "No documents have been added yet. Please upload documents first."

    try:
        return qa_chain.run(query)
    except Exception as e:
        # Catch any LLM or vectorstore errors
        return f"Error: {str(e)}"
