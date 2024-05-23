import openai
import os


from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_text(model: str, audio_file) -> str:
    res = openai.audio.transcriptions.create(
        model=model,
        file=audio_file,
    )

    return res.text
