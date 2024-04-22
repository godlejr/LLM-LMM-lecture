from enum import Enum


class PromptTemplates(str, Enum):
    MESSAGE_PROMPT = """
    This is a message from the Fastcampus e-commerce chatbot's user
    
    User: {message}
    Customer Center Staff: 
    """
