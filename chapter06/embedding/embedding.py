from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
import bs4

load_dotenv()

# collection definition
# Persistent Directory for embedding
COLLECTION_NAME = "basic_vectordb"
PERSIST_DIRECTORY = "./../../database/chroma"


# text docs
def embedding_from_text(file_path: str) -> dict:
    loader = TextLoader(file_path, encoding="utf-8")
    text = loader.load()
    docs = CharacterTextSplitter(chunk_size=250, chunk_overlap=100).split_documents(
        text
    )
    return chroma_create(docs, COLLECTION_NAME, PERSIST_DIRECTORY)


# web docs
def embedding_from_url(url: str) -> dict:
    loader = WebBaseLoader(
        web_path=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                "div",
                attrs={
                    "class": ["newsct_article _article_body", "media_end_head_headline"]
                },
            )
        ),
    )

    # crawling result
    text = loader.load()

    docs = CharacterTextSplitter(chunk_size=250, chunk_overlap=100).split_documents(
        text
    )

    return chroma_create(docs, COLLECTION_NAME, PERSIST_DIRECTORY)


def chroma_create(docs: list[str], collection_name: str, persist_diectory: str):
    result = Chroma.from_documents(
        documents=docs,
        # text-embedding-3-large - default
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        collection_name=collection_name,
        persist_directory=persist_diectory,
    )

    return result


if __name__ == "__main__":

    # url = "https://n.news.naver.com/article/437/0000388484?sid=102"
    # chromaDB = embedding_from_url(url)

    # docs = chromaDB.similarity_search("당정역 사고")

    # retrieve object

    chromaDB = embedding_from_text("./../../database/products.txt")

    retriever = chromaDB.as_retriever()
    docs = retriever.get_relevant_documents("패캠 냉장고")

    print(docs)
