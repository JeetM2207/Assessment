
#for structured input and output


from pydantic import BaseModel
from typing import List, Literal

class ContentRequest(BaseModel):
    grade: int
    topic: str

class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class GeneratorOutput(BaseModel):
    explanation: str
    mcqs: List[MCQ]

class ReviewerFeedback(BaseModel):
    status: Literal["pass", "fail"]
    feedback: List[str]