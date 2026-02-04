from langchain_google_genai import ChatGoogleGenerativeAI
from schema import GeneratorOutput, ReviewerFeedback
from dotenv import load_dotenv
load_dotenv()
import os
class ReviewerAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=api_key
        )

    def review(self, content: GeneratorOutput, grade: int, context: str) -> ReviewerFeedback:
       prompt = f"""
    You are a Wise Educational Auditor for Grade {grade} students (approx. {grade + 5} years old).
    
    GUIDELINES:
    1. NCERT CONTEXT: Use the provided text below as a guide for academic standards (Math, Science, Language).
    2. COMMON SENSE: For general topics (e.g., Teachers, Family, Seasons), allow them even if they aren't in the NCERT text, provided the language is very simple.
    3. LANGUAGE AUDIT: This is your #1 priority. Fail if the text uses "adult" words (e.g., 'foundational', 'pedagogy', 'numerical').
    4. CONCEPT CHECK: Fail only if the concept is far too advanced (e.g., teaching 1st graders about 'Atmospheric Pressure' or 'Multiplication').

    --- NCERT REFERENCE ---
       {context}
    ---

    --- CONTENT TO REVIEW ---
       {content.model_dump_json()}

    STRICT INSTRUCTION: 
    Do not fail a topic like 'Teacher' or 'School' just because the NCERT text doesn't define them. Every Grade 1 student knows what a teacher is. 
    ONLY fail if the EXPLANATION or QUESTIONS are too hard to read or understand.
    """
    
       structured_llm = self.llm.with_structured_output(ReviewerFeedback)
       return structured_llm.invoke(prompt)