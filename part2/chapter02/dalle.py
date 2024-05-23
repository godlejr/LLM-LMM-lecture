import openai
import os

from io import BytesIO
from PIL import Image
import base64

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


def get_image_b64(model: str, messgae: str):
    res = openai.images.generate(
        model=model,
        prompt=messgae,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json",  # response_format="url"로 하면 url을 반환 default
        # dalle 3 경우,
        # style="vivid"
    )

    return res.data[0].b64_json


def get_image_from_b664(b64: str) -> Image:
    image = Image.open(BytesIO(base64.b64decode(b64)))
    return image


def get_image_variation(bytes: BytesIO):
    res = openai.images.create_variation(
        model="dall-e-2",
        image=bytes,
        n=1,
        size="1024x1024",
    )

    return res.data[0].url


def get_byte_array_from_image(file_path: str) -> BytesIO:
    image = Image.open(file_path)
    width, height = 256, 256

    image = image.resize((width, height))

    bytes = BytesIO()
    image.save(bytes, format="PNG")

    return bytes.getvalue()


if __name__ == "__main__":
    # print(get_image_url("dall-e-2", "a cute cat"))

    # print(get_image_b64("dall-e-2", "a cute cat"))

    # print(get_image_from_b664(get_image_b64("dall-e-2", "a cute cat")))

    print(get_image_variation(get_byte_array_from_image("./img/cat.png")))
