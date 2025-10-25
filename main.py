# main.py

from fastapi import FastAPI, Form, Depends
from sqlalchemy.orm import Session
from models import Document, SessionLocal
from agent import add_document, ask_question, init_vectorstore

app = FastAPI()

# Initialize FAISS/QA on startup
@app.on_event("startup")
def startup_event():
    init_vectorstore()


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the FAISS + FastAPI RAG API. Use /docs to explore endpoints."}


# Upload document endpoint
@app.post("/upload")
async def upload_document(
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    # Save to database
    doc = Document(title=title, content=content)
    db.add(doc)
    db.commit()

    # Add to FAISS
    add_document(title, content)

    return {"message": "Document added successfully"}


# Query endpoint
@app.get("/query")
def query(q: str):
    answer = ask_question(q)
    return {"question": q, "answer": answer}
    
# # Run uvicorn safely on Windows
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))  # Use Render's PORT or default 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port)

