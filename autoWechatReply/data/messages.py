import warnings
from pathlib import Path
from typing import Optional, Union

import polars as pl
import tiktoken


def num_tokens_from_string(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


class chatMessages:
    USE_COLUMNS = [
        "Type",
        "SubType",
        "IsSender",
        "StrContent",
        "CreateTime",
        "StrTime",
        "Remark",
        "NickName",
        "Sender",
    ]

    def __init__(self, file_path: Union[str, Path]):
        """
        Args:
            file_path (Union[str, Path]): chatMessage file path.
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        self.file_path = file_path

        # TODO: support more type
        # only support text messages for now
        self.chat_messages = (
            pl.scan_csv(self.file_path)
            .select(self.USE_COLUMNS)
            .filter(pl.col("Type") == 1)
        )

    def get_chat_history(
        self,
        remark: Optional[str] = None,
        nickname: Optional[str] = None,
        limit=None,
        return_token: bool = False,
    ) -> pl.DataFrame:
        """get one of your friends chat history

        Args:
            remark (Optional[str], optional): wechat remark. Defaults to None.
            nickname (Optional[str], optional): wechat nickname. Defaults to None.

        Raises:
            ValueError: both remark and nickname are None.

        Returns:
            pl.DataFrame: chat history.
        """
        if not remark and not nickname:
            raise ValueError("Either `remark` or `nickname` must be provided.")
        if remark and nickname:
            warnings.warn("both remark and nickname are used for getting chat history")
            filters = (pl.col("Remark") == remark) | (pl.col("NickName") == nickname)
        if remark:
            filters = pl.col("Remark") == remark
        else:
            filters = pl.col("NickName") == nickname

        messages = self.chat_messages.filter(filters).sort("CreateTime")

        if limit:
            messages = messages.tail(limit)
        if not return_token:
            return messages
        all_content = messages.select("StrContent").collect().to_dict()["StrContent"]
        tokens = num_tokens_from_string(''.join(all_content))
        return (messages.collect(), tokens)
