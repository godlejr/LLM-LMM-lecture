from langchain.chains import LLMChain, SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from enums import PromptTemplates


# opanai chat model
chatOpenAI = ChatOpenAI(temperature=0.9, max_tokens=1000, model="gpt-3.5-turbo")


def get_llm_chain(llm, template, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(template),
        output_key=output_key,
        verbose=True,
    )


title_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.TITLE_PROMPT,
    "title",
)

plot_chain = get_llm_chain(
    chatOpenAI,
    PromptTemplates.PLOT_PROMPT,
    "plot",
)

# Multi-chain
title_plot_chain = SequentialChain(
    chains=[title_chain, plot_chain],
    input_variables=["characters", "requirements"],
    output_variables=["title", "plot"],
    verbose=True,
)
