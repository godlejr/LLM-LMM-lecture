from enum import Enum


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
