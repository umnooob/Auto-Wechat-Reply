from abc import ABC
from typing import List

import langchain
from langchain_community.document_loaders import PolarsDataFrameLoader
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

langchain.debug = True


def load_data(data) -> List[Document]:
    documents = PolarsDataFrameLoader(data, page_content_column="StrContent").load()
    return documents


def _format_chat_history(chat_history) -> List:
    buffer = []
    for doc in chat_history:
        if doc.metadata["IsSender"] == 1:
            buffer.append(HumanMessage(content=doc.page_content))
        else:
            buffer.append(AIMessage(content=doc.page_content))
    return buffer


def auto_reply(llm: BaseChatModel, question: str, chat_messages):

    docs = load_data(chat_messages)
    chat_history = _format_chat_history(docs)
    print(chat_history)
    ANSWER_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="你是一个自动回复助手，不要暴露这一点，请模仿历史回复的语气和用语习惯回复聊天消息"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{question}"),
        ]
    )
    ANSWER_PROMPT = ANSWER_PROMPT.partial(chat_history=chat_history)
    chain = ANSWER_PROMPT | llm | StrOutputParser()
    responce = chain.invoke({"question": question})
    return responce
