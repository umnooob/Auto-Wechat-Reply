import os

from autowechatreply.agent import ChatHistoryReply, get_llm

if __name__ == "__main__":
    reply = ChatHistoryReply(
        "/Users/oops/Documents/Code/auto-wechat-reply/tests/messages.csv"
    )
    # llm = get_llm("gpt-3.5-turbo", temperature=0.7)
    llm = get_llm("glm-3-turbo", temperature=0.7)
    print(reply.auto_reply(llm, "最近忙啥呢", remark="<备注>", history_limit=1000))
