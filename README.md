## 微信克隆人自动回复
基于历史对话回复好友消息

支持大模型：chatGPT、deepseek-chat、chatGLM

## 使用

### 导出聊天记录

使用[WeChatMsg](https://github.com/LC044/WeChatMsg)导出csv格式微信聊天记录

参考教程： [数据导出 | MemoTrace](https://memotrace.cn/doc/posts/deploy/exporter.html)

### 本地使用/Colab

[google colab](https://colab.research.google.com/drive/1V5aquQzg3mm67YIR_CmAcmQswDRE69FY?usp=sharing)

```bash
python interface.py
```

- nickname：微信好友昵称
- remark：微信好友备注

### 微信接入
安装autoWechatReply库后，将`./wechat`下所有内容复制粘贴加入plugins

参考 https://github.com/zhayujie/chatgpt-on-wechat/tree/master/plugins#%E6%8F%92%E4%BB%B6%E5%AE%89%E8%A3%85%E6%96%B9%E6%B3%95

并填写config.json:
```json
{
    "path": "导出聊天记录路径",
    "model": "LLM模型名称",
    "api_key": "对应模型的api key"
}
```
## TODO
- [x] 支持微信接口
- [ ] 支持除文本外的聊天回复
- [ ] 支持聊天冷启动
- [ ] 支持更多大模型

## 致谢

本项目基于[LangChain](https://www.langchain.com/)开发, 聊天记录基于[WeChatMsg](https://github.com/LC044/WeChatMsg)导出

