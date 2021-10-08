from pydantic import BaseModel
from typing import *
import json


def _b2s(b: Optional[bool]) -> Optional[str]:
    """转换布尔值为字符串。"""
    return b if b is None else str(b).lower()


settings_file_name = "./settings.json"


def get_settings(app_name: str, *args: str, std: dict = None):
    if std is None:
        settings_dict = json.load(open(settings_file_name, "r"))
    else:
        settings_dict = std

    cur = settings_dict.get(app_name)

    for k in args:
        if cur is None:
            return cur
        if isinstance(cur, dict):
            cur = cur.get(k)
        elif isinstance(cur, list):
            cur = cur[int(k)]

    return cur, settings_dict
