from autowechatreply.data import chatMessages

if __name__ == "__main__":
    cm = chatMessages("/Users/oops/Documents/Code/auto-wechat-reply/tests/messages.csv")
    print(cm.get_chat_history(remark="<备注>").head())
    print(cm.get_chat_history(remark="<备注>", nickname="<昵称>").head())
    print(cm.get_chat_history(remark="<备注>", return_token=True))
    print(cm.get_chat_history().head())
