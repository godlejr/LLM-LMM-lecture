import openai
import os

from dotenv import load_dotenv

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from enums import PromptTemplates

load_dotenv()

app = fastapi.FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatInput(BaseModel):
    message: str


# opanai chat model
chatOpenAI = ChatOpenAI(temperature=0.9, max_tokens=250, model="gpt-3.5-turbo")


def get_llm_chain(llm, template, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(template),
        output_key=output_key,
        verbose=True,
    )


message_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.MESSAGE_PROMPT,
    "output",
)


@app.post("/chat")
def chat(input: ChatInput) -> str:
    request = input.model_dump()  # {"message": "Hello"}
    response = message_chain(request)["output"]
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
