from langchain.chains import LLMChain, SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from enums import PromptTemplates


# opanai chat model
chatOpenAI = ChatOpenAI(temperature=0.9, max_tokens=250, model="gpt-3.5-turbo")


def get_llm_chain(llm, template, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(template),
        output_key=output_key,
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