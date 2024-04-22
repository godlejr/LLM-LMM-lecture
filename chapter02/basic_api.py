import openai
import os

from dotenv import load_dotenv


import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn


app = fastapi.FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatInput(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 300
    temperature: float = 0.9


@app.post("/chat")
def chat(input: ChatInput) -> str:
    response = openai.chat.completions.create(
        model=input.model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input.message},
        ],
        max_tokens=input.max_tokens,
        temperature=input.temperature,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
