from langchain.chains import LLMChain, SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from enums import PromptTemplates

from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory


# opanai chat model
chatOpenAI = ChatOpenAI(temperature=0.9, max_tokens=250, model="gpt-3.5-turbo")


def get_llm_chain(llm, template, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(template),
        output_key=output_key,
        verbose=True,
    )


def get_llm_chain_for_memory(llm, template, output_key, memory):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(template),
        output_key=output_key,
        memory=memory,
        verbose=True,
    )


intent_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.INTENT_PROMPT,
    "intent",
)

analysis_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.INQUIRY_ANALYSIS_PROMPT,
    "analysis",
)

rely_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.INQUIRY_REPLY_PROMPT,
    "reply",
)

# Multi-chain
analysis_rely_chain = SequentialChain(
    chains=[analysis_chain, rely_chain],
    input_variables=["message", "guide"],
    output_variables=["analysis", "reply"],
    verbose=True,
)

purchase_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.PURCHASE_PROMPT,
    "reply",
)

complaint_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.COMPLAINT_PROMPT,
    "reply",
)

## memory
# memory = ConversationBufferMemory(
#     input_key="message",
#     output_key="reply",
#     memory_key="histories",
#     return_messages=True,  # ai message & human message set
# )

memory = ConversationBufferWindowMemory(
    k=1,
    input_key="message",
    output_key="reply",
    memory_key="histories",
    return_messages=True,  # ai message & human message set
)


default_chain = get_llm_chain_for_memory(
    chatOpenAI, PromptTemplates.DEFAULT_PROMPT, "reply", memory
)
