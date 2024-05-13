import os

from autowechatreply.agent import get_llm, get_llm_names

os.environ["DEEPSEEK_API_KEY"] = "sk-b3877eeed1ee4b2e8017ce0f02129a31"
if __name__ == "__main__":
    print(get_llm_names())
    llm = get_llm("deepseek-chat")
    print(llm.invoke("你好"))
