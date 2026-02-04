from fastapi import FastAPI, HTTPException
from schema import ContentRequest, GeneratorOutput, ReviewerFeedback
from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

app = FastAPI(title="AI Educational Content Pipeline")

# initialize Agents
generator = GeneratorAgent()
reviewer = ReviewerAgent()



# Change your embedding initialization to this:
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = PineconeVectorStore(index_name="assessment", embedding=embeddings)

def get_ncert_standards(grade: int, topic: str):
    # Search specifically for the curriculum of that grade and topic
    query = f"What are the Class {grade} learning outcomes for {topic}?"
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])

@app.post("/generate-lesson")
async def generate_lesson(request: ContentRequest):
    # 1. Fetch Ground Truth from Pinecone
    curriculum_context = get_ncert_standards(request.grade, request.topic)
    
    # 2. Generator Pass 1
    draft = generator.generate(request)
    
    # 3. Reviewer Audit (Using NCERT Context)
    review_result = reviewer.review(draft, request.grade, context=curriculum_context)
    
    # 4. Refinement Logic (Max 1 Pass)
    final_output = draft
    if review_result.status == "fail":
        final_output = generator.generate(request, feedback=review_result.feedback)

    return {
        "initial_draft": draft,
        "reviewer_feedback": review_result,
        "final_content": final_output,
        "ncert_evidence": curriculum_context # Show this in UI to impress them!
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)