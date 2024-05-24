import os

from autowechatreply.agent import get_llm, get_llm_names

if __name__ == "__main__":
    print(get_llm_names())
    llm = get_llm("deepseek-chat")
    print(llm.invoke("你好"))
