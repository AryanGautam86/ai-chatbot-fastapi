################################
# agent.py
import os
from pathlib import Path
from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv


load_dotenv()  # loads .env
OPENROUTER_KEY = os.getenv("OPENAI_API_KEY")

# USE Your OpenRouter API Key
# os.environ["OPENAI_API_KEY"] = OPENROUTER_KEY  # Required for ChatOpenAI


# Global variables (this give one shared instance for all API calls)
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
                #model="tngtech/deepseek-r1t2-chimera:free",
                model="deepseek/deepseek-r1",
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
                #model="tngtech/deepseek-r1t2-chimera:free",
                model="deepseek/deepseek-r1",
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
        response = qa_chain.invoke({"query": query})
        return response["result"]

    except Exception as e:
        # Catch any LLM or vectorstore errors
        return f"Error: {str(e)}"
        
############### AI generated

from langchain_openai import ChatOpenAI
from typing import Dict
import subprocess
#import tempfile
import os
import uuid

LANGUAGE_CONFIG = {
    "python": {"cmd": ["python"], "ext": ".py"},
    "javascript": {"cmd": ["node"], "ext": ".js"},
    "cpp": {"compile": ["g++"], "ext": ".cpp"},
    "c": {"compile": ["gcc"], "ext": ".c"},
    "java": {"compile": ["javac"], "ext": ".java"}
}

def run_code(code: str, language: str) -> str:
    language = language.lower()

    if language not in LANGUAGE_CONFIG:
        return f"Execution not supported for language: {language}"

    config = LANGUAGE_CONFIG[language]

    file_id = str(uuid.uuid4())
    ext = config["ext"]
    filename = f"{file_id}{ext}"

    try:
        with open(filename, "w") as f:
            f.write(code)

        if language in ["python", "javascript"]:
            cmd = config["cmd"] + [filename]

        elif language in ["c", "cpp"]:
            exe = f"{file_id}.out"
            compile_cmd = config["compile"] + [filename, "-o", exe]
            subprocess.check_output(compile_cmd, stderr=subprocess.STDOUT, timeout=10)
            cmd = [f"./{exe}"]

        elif language == "java":
            subprocess.check_output(["javac", filename], stderr=subprocess.STDOUT, timeout=10)
            class_name = filename.replace(".java", "")
            cmd = ["java", class_name]

        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=10)
        return output.decode()

    except subprocess.CalledProcessError as e:
        return e.output.decode()

    except Exception as e:
        return str(e)

    finally:
        for f in os.listdir():
            if f.startswith(file_id):
                os.remove(f)

def generate_code_from_prompt(user_task: str,language: str = "python",run_tests: bool = False) -> Dict:
    """
    LLM-powered dynamic code generator using OpenRouter + DeepSeek.
    Supports multi-language execution.
    """

    llm = ChatOpenAI(
        #model="tngtech/deepseek-r1t2-chimera:free",
        model="deepseek/deepseek-r1",
        temperature=0.2,
        openai_api_key=OPENROUTER_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
    )

    prompt = f"""
You are a senior software engineer.

Generate clean, correct, production-quality {language} code for the task below.

TASK:
{user_task}

Rules:
- Output ONLY code.
- No explanations.
- No markdown.
- Code must be directly runnable.
"""

    response = llm.invoke(prompt)
    code = response.content.strip()

    result = {
        "code_or_questions": f"```{language}\n{code}\n```",
        "notes": "AI-generated code using DeepSeek R1"
    }

    # Optional execution
    if run_tests:
        execution_output = run_code(code, language)
        result["execution_output"] = execution_output

    return result




    




    
