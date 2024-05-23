import openai
import os


from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_text(model: str, file_path: str) -> str:
    audio_file = open(file_path, "rb")
    res = openai.audio.transcriptions.create(
        model=model,
        file=audio_file,
    )

    return res.text


def get_english_text(model: str, file_path: str) -> str:
    audio_file = open(file_path, "rb")
    res = openai.audio.translations.create(
        model=model,
        file=audio_file,
    )
    return res.text


if __name__ == "__main__":
    # print(get_text("whisper-1", "./audio/speech-hd.mp3"))

    print(get_english_text("whisper-1", "./audio/speech-hd.mp3"))
