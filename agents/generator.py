import os
from langchain_google_genai import ChatGoogleGenerativeAI
from schema import ContentRequest, GeneratorOutput
from dotenv import load_dotenv
load_dotenv()
class GeneratorAgent:
    def __init__(self):

        api_key = os.getenv("GOOGLE_API_KEY")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=api_key
        )

    def generate(self, data: ContentRequest, feedback: list = None) -> GeneratorOutput:
        
        if not feedback:
            prompt = f"""
            Task: Create a lesson for Grade {data.grade} students.
            Topic: {data.topic}
            Requirement: Provide a clear explanation and 4 multiple-choice questions.
            """
        else:
            
            prompt = f"""
            You previously generated content for Grade {data.grade} on '{data.topic}', 
            but it was REJECTED by the Reviewer.
            
            FEEDBACK FROM REVIEWER:
            {feedback}
            
            TASK: Rewrite the explanation and MCQs to strictly follow the feedback above. 
            Ensure the language is now perfectly suited for a Grade {data.grade} student.
            """

        structured_llm = self.llm.with_structured_output(GeneratorOutput)
        return structured_llm.invoke(prompt)