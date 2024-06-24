# encoding:utf-8

import json
import os

import requests
from autowechatreply.agent import ChatHistoryReply, get_llm

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *

llm_api_keys = {
    "deepseek-chat": "DEEPSEEK_API_KEY",
    "gpt-3.5-turbo": "OPENAI_API_KEY",
    "gpt-4-turbo-preview": "OPENAI_API_KEY",
    "glm-3-turbo": "ZHIPU_API_KEY",
    "glm-4": "ZHIPU_API_KEY",
}


@plugins.register(
    name="autoreply",
    desire_priority=980,
    hidden=True,
    desc="自动克隆回复",
    version="0.1",
    author="zephan",
)
class AutoReply(Plugin):
    def __init__(self):
        super().__init__()
        try:
            curdir = os.path.dirname(__file__)
            config_path = os.path.join(curdir, "config.json")
            conf = None
            if not os.path.exists(config_path):
                logger.debug(f"[autoreply]不存在配置文件{config_path}")
                raise ValueError(f"[autoreply]不存在配置文件{config_path}")
            else:
                logger.debug(f"[autoreply]加载配置文件{config_path}")
                with open(config_path, "r", encoding="utf-8") as f:
                    conf = json.load(f)
            # 加载配置
            self.path = conf["path"]
            self.model = conf["model"]
            self.api_key = conf["api_key"]
            if self.api_key:
                os.environ[llm_api_keys[self.model]] = self.api_key

            self.autoreply = ChatHistoryReply(self.path)
            self.llm = get_llm(self.model)
            logger.info("[autoreply] file path{}".format(self.path))
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            logger.info("[autoreply] inited.")
        except Exception as e:
            logger.warn("[autoreply] init failed.")
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return

        content = e_context["context"].content.strip()
        logger.debug("[autoreply] on_handle_context. content: %s" % content)
        logger.debug("[autoreply] on_handle_context. e_context: %s" % e_context.econtext["context"]["msg"].__dict__)

        reply_text = self.autoreply.auto_reply(self.llm, content, nickname=e_context.econtext["context"]["msg"].from_user_nickname, history_limit=100)
        reply = Reply()
        reply.type = ReplyType.TEXT
        reply.content = reply_text

        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

    def get_help_text(self, **kwargs):
        help_text = "克隆回复"
        return help_text
