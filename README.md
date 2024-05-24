## 微信克隆人自动回复
基于历史对话回复好友消息

支持大模型：chatGPT、deepseek-chat、chatGLM

## 使用

### 导出聊天记录

使用[WeChatMsg](https://github.com/LC044/WeChatMsg)导出csv格式微信聊天记录

参考教程： [数据导出 | MemoTrace](https://memotrace.cn/doc/posts/deploy/exporter.html)

### 本地使用

```bash
python interface.py
```

- nickname：微信好友昵称
- remark：微信好友备注

## TODO
- [ ] 支持微信接口
- [ ] 支持除文本外的聊天回复
- [ ] 支持聊天冷启动
- [ ] 支持更多大模型

## 致谢

本项目基于[LangChain](https://www.langchain.com/)开发, 聊天记录基于[WeChatMsg](https://github.com/LC044/WeChatMsg)导出

