from pydantic import BaseModel
from typing import *


def _b2s(b: Optional[bool]) -> Optional[str]:
    """转换布尔值为字符串。"""
    return b if b is None else str(b).lower()


