import openai
import base64
import requests
import os

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_vision_from_single_image(
    model: str, prompt: str, image_url: str, max_tokens: int
) -> str:
    res = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            },
        ],
        max_tokens=max_tokens,
    )

    return res.choices[0].message.content


def get_vision_from_multiple_images(
    model: str, prompt: str, image_urls: list, max_tokens: int
) -> str:
    res = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    *[
                        {"type": "image_url", "image_url": {"url": image_url}}
                        for image_url in image_urls
                    ],
                ],
            },
        ],
        max_tokens=max_tokens,
    )

    return res.choices[0].message.content


def get_vision_from_single_image_base64(
    model: str, prompt: str, base64_image: str, max_tokens: int
) -> str:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64, {base64_image}",
                        },
                    },
                ],
            },
        ],
        "max_tokens": max_tokens,
    }

    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    print(res)

    return res.json()["choices"][0]["message"]["content"]


# 이미지를 base64로 인코딩하는 함수
def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    print(
        get_vision_from_single_image(
            "gpt-4o",
            "이미지에 대해 설명해주세요",
            "https://upload.wikimedia.org/wikipedia/commons/d/d8/Railings_7m_from_NW_corner_of_Assembly_of_God_Pentecostal_Church_York_03.jpg",
            300,
        )
    )

    # image_urls = [
    #     "https://upload.wikimedia.org/wikipedia/commons/f/f7/Female_Football_01.jpg",
    #     "https://upload.wikimedia.org/wikipedia/commons/f/f3/Female_Football_02.jpg",
    # ]

    # print(
    #     get_vision_from_multiple_images(
    #         "gpt-4-turbo", "연속된 이미지에 대해 설명해주세요", image_urls, 300
    #     )
    # )

    # image_path = "./img/cat.png"

    # print(
    #     get_vision_from_single_image_base64(
    #         "gpt-4-turbo", "이미지에 대해 설명해주세요", encode_image(image_path), 300
    #     )
    # )
