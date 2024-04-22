from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

from enums import ChromaDB

# initialize the chroma
chroma = Chroma(
    persist_directory=ChromaDB.PERSIST_DIRECTORY,
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name=ChromaDB.COLLECTION_NAME,
)

retriever = chroma.as_retriever()


def get_relevant_documents(query: str) -> List[str]:
    documents = retriever.get_relevant_documents(query)
    content_of_documents = [doc.page_content for doc in documents]
    return content_of_documents
