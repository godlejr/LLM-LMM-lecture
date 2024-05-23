import openai
import os

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_image_url(model: str, messgae: str):
    res = openai.images.generate(
        model=model,
        prompt=messgae,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="url",
        # dalle 3 경우,
        # style="vivid"
    )

    return res.data[0].url
