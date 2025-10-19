# ai-chatbot-fastapi
- A FastAPI-based AI assistant powered by LangChain and vector search for retrieval-augmented question answering. Containerized with Docker for easy deployment.

# Features
- Conversational AI with LangChain
- Retrieval-augmented answers using FAISS or other vector stores
- Modular FastAPI backend
- Containerized with Docker for production-ready deployment
- Easy to extend with new models or embeddings

# Set-Up
- make clean environment and download all dependencies
- Make sure you have all these file
- Use your Open-api key (my use limit exceed)
- You can upload data and as well as get access data just by run [uvicorn main:app --reload].
- open \docs in browser and you can upload by post and get querry by Get.
- For Dockerize the model make requirements.txt file and docker file.
- For building run [docker build -t ai-chatbot-fastapi .]
- for running container run [docker run -p 8000:8000 ai-chatbot-fastapi]

