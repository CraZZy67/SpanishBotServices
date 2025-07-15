from fastapi import FastAPI
from pydantic import BaseModel

from agent_ import Agent


class PromptParam(BaseModel):
    format: str
    level: str
    countries: str
    language: str

app = FastAPI(debug=True)

@app.post('/generate/')
def generate_content(prompt: PromptParam):

    return {'answer': 'ю.! Сгенерированный текст **Привет**, ||ХАЙ||'}
    # return Agent.generate_post(**prompt.model_dump())