# agent.py
import os

# Set OpenAI API key [Use Your Open-api Key my use limit quota is finished]
os.environ["OPENAI_API_KEY"] = "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"


from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

vectorstore = None
qa_chain = None
embedding_model = None

def init_vectorstore():
    """
    Initialize FAISS vectorstore and QA chain.
    Must be called after first document or on startup.
    """
    global vectorstore, qa_chain, embedding_model

    # os.environ["OPENAI_API_KEY"] = "Use Your API key"

    # Initialize HuggingFace embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists("faiss.index"):
        vectorstore = FAISS.load_local("faiss.index", embedding_model, allow_dangerous_deserialization=True)
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
        )
    else:
        vectorstore = None
        qa_chain = None


def add_document(title: str, content: str):
    """
    Add a new document to the FAISS vectorstore and save the index.
    """
    global vectorstore, qa_chain, embedding_model

    if embedding_model is None:
        init_vectorstore()

    if vectorstore is None:
        # First document, create new vectorstore
        vectorstore = FAISS.from_texts([content], embedding=embedding_model, metadatas=[{"title": title}])
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
        )
    else:
        # Add to existing vectorstore
        vectorstore.add_texts([content], metadatas=[{"title": title}])

    # Save the FAISS index
    vectorstore.save_local("faiss.index")


def ask_question(query: str):
    """
    Ask a question using the RAG chain.
    """
    global qa_chain, vectorstore

    if vectorstore is None or qa_chain is None:
        return "No documents have been added yet. Please upload documents first."

    return qa_chain.run(query)

