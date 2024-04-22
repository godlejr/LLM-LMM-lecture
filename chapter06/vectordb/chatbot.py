import openai
import os

from dotenv import load_dotenv

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn

from chains import intent_chain, analysis_rely_chain, purchase_chain
from vectordb import get_relevant_documents


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


# dto
class ChatInput(BaseModel):
    message: str


# API 를 통한 RAG 생성 1
def get_intents() -> str:
    # requests.get("https://api.example.com/intents")
    return """
    - purchase
    - inquiry
    - complaint
    """


# API 를 통한 RAG 생성 2
def get_customer_center_guide() -> str:
    # guide = requests.get("https://api.example.com/guide/2024")
    return f"""
    2024, Customer Center Guide
    - inquiry about the microwave is no answered (because of absence of the staff)
    - inquiry the cooker is available
    """


@app.post("/chat")
def chat(input: ChatInput) -> str:
    common_msg = f"""
    iam sorry, i am not able to understand your message
    """
    # req
    # {"message": "안녕하세요", "intents" : "purchase, inquiry, complaint"}
    req = input.model_dump()
    req["intents"] = get_intents()

    intent = intent_chain(req)["intent"]
    print(intent)

    if intent == "complaint":
        COMPLAINT_RESPONSE = f"""
        I'm sorry to hear that you're having trouble.
        """
        return COMPLAINT_RESPONSE

    if intent == "purchase":
        req["relevant_documents"] = get_relevant_documents(req["message"])
        purchase_reply = purchase_chain(req)["reply"]
        return purchase_reply

    if intent == "inquiry":
        req["guide"] = get_customer_center_guide()
        analysis_rely = analysis_rely_chain(req)["reply"]

        return analysis_rely

    return common_msg


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
