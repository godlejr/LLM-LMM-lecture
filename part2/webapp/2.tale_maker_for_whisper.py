import requests
import streamlit as st

from whisper import get_text

API_URL = "http://localhost:8000/tales"


DEFAULT_OF_CHARACTERS = "시골소녀, 도시소년"
DEFAULT_OF_REQUIREMENTS = "시골소녀는 도시소년를 만나고 싶어함"

# input
if "characters" not in st.session_state:
    st.session_state.characters = DEFAULT_OF_CHARACTERS

if "requirements" not in st.session_state:
    st.session_state.requirements = DEFAULT_OF_REQUIREMENTS

if "whisper_audio" not in st.session_state:
    st.session_state.whisper_audio = []


# output

if "title" not in st.session_state:
    st.session_state.title = ""

if "plot" not in st.session_state:
    st.session_state.plot = ""

if "image" not in st.session_state:
    st.session_state.image = []


def make_tale(characters: str, requirements: str) -> dict:
    data = {"characters": characters, "requirements": requirements}
    response = requests.post(API_URL, json=data)

    return response.json()


def get_sidebar_ui():
    with st.sidebar:
        # input

        st.subheader("등장 인물 입력")
        characters = st.text_area(
            "ex).인물1, 인물2, 인물3", st.session_state.characters
        )
        st.session_state.characters = characters

        st.subheader("요구 사항 입력")

        # input whisper audio
        st.session_state.whisper_audio = st.file_uploader(
            "요구사항 음성 파일 업로드", type=["mp3"]
        )

        print(st.session_state.whisper_audio)

        if st.session_state.whisper_audio:
            st.session_state.requirements = get_text(
                "whisper-1", st.session_state.whisper_audio
            )

        requirements = st.text_area(
            "ex). 러브스토리가 있었으면 좋겠습니다.", st.session_state.requirements
        )
        st.session_state.requirements = requirements

        if st.button("동화책 만들기"):
            res = make_tale(st.session_state.characters, st.session_state.requirements)

            st.session_state.title = res["title"]
            st.session_state.plot = res["plot"]

            # url
            st.session_state.image = res["image"]


def get_result_ui():
    # output
    st.title(st.session_state.title)

    st.image(st.session_state.image)

    st.write(st.session_state.plot)


if __name__ == "__main__":
    # input
    get_sidebar_ui()
    # output
    get_result_ui()
