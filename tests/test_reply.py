import os

from autowechatreply.agent import auto_reply, get_llm, load_data
from autowechatreply.data import chatMessages

if __name__ == "__main__":
    cm = chatMessages(
        "/Users/oops/Documents/Code/auto-wechat-reply/tests/messages.csv"
    ).get_chat_history(remark="陈俊龙", limit=1000)
    # llm = get_llm("gpt-3.5-turbo", temperature=0.7)
    llm = get_llm("deepseek-chat", temperature=0.7)
    print(auto_reply(llm, "最近忙啥呢", cm))
