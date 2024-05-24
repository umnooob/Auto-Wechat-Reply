import os

import gradio as gr

from autowechatreply.agent import ChatHistoryReply, LLMType, get_llm, get_llm_names

llm_api_keys = {
    "deepseek-chat": "DEEPSEEK_API_KEY",
    "gpt-3.5-turbo": "OPENAI_API_KEY",
    "gpt-4-turbo-preview": "OPENAI_API_KEY",
    "glm-3-turbo": "ZHIPU_API_KEY",
    "glm-4": "ZHIPU_API_KEY",
}


class ChatApp:
    def __init__(self):
        self.reply: ChatHistoryReply = None

    def answer(
        self,
        message,
        history,
        llm,
        api_key=None,
        remark=None,
        nickname=None,
        history_limit=None,
    ):
        if api_key:
            os.environ[llm_api_keys[llm]] = api_key
        llm = get_llm(llm)
        self.reply.prefetch_history(
            remark=remark, nickname=nickname, history_limit=history_limit
        )
        gr.Warning(f"使用 {len(self.reply.chat_history)}条聊天记录")
        return self.reply.auto_reply(llm, message)

    def upload_file(self, filepath):
        self.reply = ChatHistoryReply(filepath)
        return (
            gr.update(visible=False),
            gr.update(visible=True),
        )


chat_app = ChatApp()


def update_api_key_input(llm_selection):
    api_key_field_name = llm_api_keys.get(llm_selection, None)
    if api_key_field_name:
        return gr.Textbox(
            label=f"{api_key_field_name}",
            placeholder=f"请输入您的{api_key_field_name}",
            visible=True,
        )
    else:
        return gr.Textbox(visible=False)


with gr.Blocks() as app:
    with gr.Group(visible=False) as chatbot_group:
        dropdown = gr.Dropdown(get_llm_names(), label="LLM", info="Choose LLM")
        api_key = gr.Textbox(visible=False)
        chatbot = gr.ChatInterface(
            chat_app.answer,
            additional_inputs=[
                dropdown,
                api_key,
                gr.Textbox(
                    label="微信备注", placeholder="微信备注或微信昵称填一个即可"
                ),
                gr.Textbox(
                    label="微信昵称", placeholder="微信备注或微信昵称填一个即可"
                ),
                gr.Number(value=500, label="使用的记录条数"),
            ],
        )
        dropdown.select(
            update_api_key_input,
            inputs=[dropdown],
            outputs=[api_key],
        )
    with gr.Group() as upload_group:
        file = gr.File(file_count="single", file_types=["csv"])
        file.upload(
            chat_app.upload_file,
            inputs=[file],
            outputs=[upload_group, chatbot_group],
            show_progress=True,
        )

if __name__ == "__main__":
    app.launch(share=True)
