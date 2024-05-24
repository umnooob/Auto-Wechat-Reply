from abc import ABC
from pathlib import Path
from typing import List, Optional, Union

import langchain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PolarsDataFrameLoader
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from autowechatreply.data import chatMessages

langchain.debug = True


class ChatHistoryReply:
    def __init__(self, file_path: Union[str, Path]) -> None:
        self.message = chatMessages(file_path)
        self.chat_history = None

    @staticmethod
    def _format_chat_history(chat_history) -> List:
        buffer = []
        for doc in chat_history:
            if doc.metadata["IsSender"] == 1:
                buffer.append(HumanMessage(content=doc.page_content))
            else:
                buffer.append(AIMessage(content=doc.page_content))
        return buffer

    def prefetch_history(
        self,
        remark: Optional[str] = None,
        nickname: Optional[str] = None,
        history_limit: Optional[int] = None,
    ):
        chat_messages = self.message.get_chat_history(
            remark=remark, nickname=nickname, limit=history_limit
        )
        docs = PolarsDataFrameLoader(
            chat_messages, page_content_column="StrContent"
        ).load()

        self.chat_history = self._format_chat_history(docs)
        return self.chat_history

    def auto_reply(
        self,
        llm: BaseChatModel,
        question: str,
        remark: Optional[str] = None,
        nickname: Optional[str] = None,
        history_limit: Optional[int] = None,
        memory=True,
    ):
        if not self.chat_history:
            self.prefetch_history(
                remark=remark, nickname=nickname, history_limit=history_limit
            )

        ANSWER_PROMPT = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="你是一个自动回复助手，不要暴露这一点，请伪装成我，模仿历史回复的语气和用语习惯回复聊天消息"
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{question}"),
            ]
        )
        ANSWER_PROMPT = ANSWER_PROMPT.partial(chat_history=self.chat_history)
        chain = ANSWER_PROMPT | llm | StrOutputParser()
        responce = chain.invoke({"question": question})
        self.chat_history.extend(
            [HumanMessage(content=question), AIMessage(content=responce)]
        )
        return responce
