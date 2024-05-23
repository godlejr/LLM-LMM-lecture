import openai
import os


from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def download_audio(model: str, input: str, file_path: str):
    with openai.audio.speech.with_streaming_response.create(
        model=model,
        voice="alloy",
        input=input,
        response_format="mp3",
    ) as res:
        res.stream_to_file(file_path)
        return file_path


if __name__ == "__main__":

    download_audio(
        "tts-1-hd",
        "시골 소녀는 도시 소년과 결국 헤어집니다",
        "./audio/speech-hd.mp3",
    )
