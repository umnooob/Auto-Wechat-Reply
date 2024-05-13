from autowechatreply.data import chatMessages

if __name__ == "__main__":
    cm = chatMessages("/Users/oops/Documents/Code/auto-wechat-reply/tests/messages.csv")
    print(cm.get_chat_history(remark="周浩").head())
    print(cm.get_chat_history(remark="周浩", nickname="浩er🌊").head())
    print(cm.get_chat_history(remark="周浩", return_token=True))
    print(cm.get_chat_history().head())
