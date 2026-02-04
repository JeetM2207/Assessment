# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the local embedding model during build so it's ready
RUN python -c "from langchain_huggingface import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')"

# Copy all project files (including agents, PDFs, and schema)
COPY . .

# Create a shell script to run both FastAPI and Streamlit
RUN echo '#!/bin/bash\n\
uvicorn api_server:app --host 0.0.0.0 --port 8000 &\n\
streamlit run ui_app.py --server.port 7860 --server.address 0.0.0.0\n\
' > start.sh && chmod +x start.sh

# Hugging Face Spaces usually runs on port 7860
EXPOSE 7860

# Run the startup script
CMD ["./start.sh"]