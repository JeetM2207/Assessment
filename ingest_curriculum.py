import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

file_paths = ["elementary_standards.pdf", "secondary_standards.pdf"]
docs = []
for path in file_paths:
    if os.path.exists(path):
        docs.extend(PyPDFLoader(path).load())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "assessment"

print(f"Starting ingestion of {len(splits)} chunks...")
vectorstore = PineconeVectorStore.from_documents(
    splits, 
    embeddings, 
    index_name=index_name
)
print(" Done! Everything is in Pinecone.")