from enum import Enum


class ChromaDB(str, Enum):
    COLLECTION_NAME = "basic_vectordb"
    PERSIST_DIRECTORY = "./../../database/chroma"


class PromptTemplates(str, Enum):
    INTENT_PROMPT = """
    choose the one of the following intents for the user message
    [intents]
    {intents}
    
    User : i have a problem, your service is aweful
    classifier : complaint
    
    User: {message}
    classifier : 
    """

    INQUIRY_ANALYSIS_PROMPT = """
    analyze the user's message for inquiry
    
    User: {message}
    Analysis :
    """

    INQUIRY_REPLY_PROMPT = """
    reply to the user's inquiry message with inquiry analysis and Customer Center Guide
    
    [inquiry analysis]
    {analysis}
    
    [Customer Center Guide]
    {guide}
    
    User: {message}
    Reply: 
    """

    PURCHASE_PROMPT = """
    relay the user's purchase message with the following product details
    
    [product details]
    {relevant_documents}
    
    User: {message}
    Reply: 
    """

    COMPLAINT_PROMPT = """
    reply to the user's complaint message with extraction message-related from web search solution 
    
    [web search solution]
    {search_result}
    
    User: {message}
    Reply: 
    """
