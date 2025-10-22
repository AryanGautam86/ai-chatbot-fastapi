##################################
# # official Python image
# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Copy requirements first for caching
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# # Copy all project files
# COPY . .

# # Expose FastAPI port
# EXPOSE 8000

# # Set environment variable for OpenRouter API key
# ENV OPENAI_API_KEY="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"

# # Command to run FastAPI with Uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
##################################
# Base image with PyTorch preinstalled
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies (skip torch to save time)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Set environment variable for OpenRouter API key
#ENV OPENAI_API_KEY="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"

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
