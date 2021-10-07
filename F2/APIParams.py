from pydantic import BaseModel
from typing import *
from utils.utils import _b2s
from F2.Message import Message, MessageSegment

from pygtrie import StringTrie
import inspect

'''
# API

```json
{
    "action": "send_private_msg",
    "params": {
        "user_id": 10001000,
        "message": "你好"
    },
    "echo": "123"
}
```
'''


class APIParams(BaseModel):
    __apiname__ = ""


class SendPrivateMsg(APIParams):
    __apiname__ = "send_private_msg"
    user_id: int
    message: Union[Message, str]
    auto_escape: Optional[bool]


class SendGroupMsg(APIParams):
    __apiname__ = "send_group_msg"
    group_id: int
    message: Union[Message, str]
    auto_escape: Optional[bool]


class SendMsg(APIParams):
    __apiname__ = "send_msg"
    message_type: Optional[Literal["private", "group"]]
    user_id: Optional[int]
    group_id: Optional[int]
    message: Union[Message, str]
    auto_escape: Optional[bool]


class DeleteMsg(APIParams):
    __apiname__ = "delete_msg"
    message_id: int


class GetMsg(APIParams):
    __apiname__ = "get_msg"
    message_id: int


class GetForwardMsg(APIParams):
    __apiname__ = "get_forward_msg"
    id: str


class SendLike(APIParams):
    __apiname__ = "send_like"
    user_id: int
    times: Optional[int]


class SetGroupKick(APIParams):
    __apiname__ = "set_group_kick"
    group_id: int
    user_id: int
    reject_add_request: Optional[bool]


class SetGroupBan(APIParams):
    __apiname__ = "set_group_ban"
    group_id: int
    user_id: int
    duration: Optional[int]


# Find APIParams
_trie = StringTrie(separator=".")
for apiparamsmodel in list(globals().values()):
    if inspect.isclass(apiparamsmodel) and issubclass(apiparamsmodel, APIParams):
        _trie["." + apiparamsmodel.__apiname__] = apiparamsmodel


def get_apiparams_model(apiname: str) -> List[Type[APIParams]]:
    # [::-1] ： 把列表倒着弄
    return [model.value for model in _trie.prefixes("." + apiname)][::-1]
