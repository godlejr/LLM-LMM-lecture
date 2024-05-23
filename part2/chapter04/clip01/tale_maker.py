import openai
import os

from dotenv import load_dotenv


import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn

from chains import title_plot_chain
from enums import Dalles
from dalle import get_image_url


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


class TaleInput(BaseModel):
    characters: str
    requirements: str


def get_tale_image_prompt_from_param(
    characters: str, requirements: str, title: str
) -> str:
    image_prompt = Dalles.IMAGE_PROMPT
    image_prompt += f"""
    [characters] 
    {characters}
    
    [requirements]
    {requirements}
    
    [title]
    {title}
    """
    return image_prompt


@app.post("/tales")
def chat(input: TaleInput) -> dict:
    req = input.model_dump()  # dict 형태로 변환
    res = title_plot_chain(req)

    res["image"] = get_image_url(
        "dall-e-3",
        get_tale_image_prompt_from_param(
            res["characters"], res["requirements"], res["title"]
        ),
    )

    return res


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
