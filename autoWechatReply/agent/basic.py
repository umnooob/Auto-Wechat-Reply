import os
from enum import Enum

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


class LLMType(str, Enum):
    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4-turbo-preview"
    DEEPSEEK = "deepseek-chat"
    CHATGLM3 = "glm-3-turbo"
    CHATGLM4 = "glm-4"


OPENAI_TYPES = [LLMType.GPT3_5, LLMType.GPT4]
DEEPSEEK_TYPES = [LLMType.DEEPSEEK]
CHATGLM_TYPES = [LLMType.CHATGLM3, LLMType.CHATGLM4]


def get_llm(name: LLMType, temperature=0.7) -> BaseChatModel:
    if name in OPENAI_TYPES:
        return ChatOpenAI(name=name, temperature=temperature)
    elif name in DEEPSEEK_TYPES:
        return ChatOpenAI(
            model=name,
            temperature=temperature,
            openai_api_base="https://api.deepseek.com/v1",
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        )
    elif name in CHATGLM_TYPES:
        return ChatOpenAI(
            model=name,
            temperature=temperature,
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
            openai_api_key=os.getenv("ZHIPU_API_KEY"),
        )
    else:
        raise ValueError(f"Not Implement LLM `{name}`")


def get_llm_names():
    return [name.value for name in LLMType]
