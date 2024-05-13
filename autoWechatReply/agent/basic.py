import os
from enum import Enum

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


class LLMType(str, Enum):
    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4-turbo-preview"
    DEEPSEEK = "deepseek-chat"


openai = [LLMType.GPT3_5, LLMType.GPT4]
deepseek = [LLMType.DEEPSEEK]


def get_llm(name: LLMType, temperature=1.1) -> BaseChatModel:
    if name in openai:
        return ChatOpenAI(name=name, temperature=temperature)
    elif name in deepseek:
        return ChatOpenAI(
            model=name,
            temperature=temperature,
            openai_api_base="https://api.deepseek.com/v1",
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        )
    else:
        raise ValueError(f"Not Implement LLM `{name}`")


def get_llm_names():
    return [name.value for name in LLMType]
