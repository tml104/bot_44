from pydantic import BaseModel
from typing import *
from utils.utils import _b2s
from F2.Message import Message, MessageSegment
from pygtrie import StringTrie
import inspect


class Event(BaseModel):
    __event__ = ""
    time: int
    self_id: int
    post_type: str


# Models
class Sender(BaseModel):
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    card: Optional[str] = None
    sex: Optional[Literal["male", "female", "unknown"]] = None
    age: Optional[int] = None
    area: Optional[str] = None
    level: Optional[str] = None
    role: Optional[Literal["owner", "admin", "member"]] = None
    title: Optional[str] = None

    class Config:
        extra = "allow"


class Reply(BaseModel):
    time: int
    message_type: str
    message_id: int
    real_id: int
    sender: Sender
    message: Message

    class Config:
        extra = "allow"


class Anonymous(BaseModel):
    id: int
    name: str
    flag: str

    class Config:
        extra = "allow"


class File(BaseModel):
    id: str
    name: str
    size: int
    busid: int
    url: str

    class Config:
        extra = "allow"


class Device(BaseModel):
    app_id: int
    device_name: str
    device_kind: str

    class Config:
        extra = "allow"


class Status(BaseModel):
    online: bool
    good: bool

    class Config:
        extra = "allow"


# Message Events
class MessageEvent(Event):
    """消息事件"""
    __event__ = "message"
    post_type: Literal["message"]
    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    message: Message
    raw_message: str
    font: int
    sender: Sender


class PrivateMessageEvent(MessageEvent):
    """私聊消息"""
    __event__ = "message.private"
    message_type: Literal["private"]
    sub_type: Literal["friend", "group", "group_selg", "other"]
    temp_source: Optional[int] = None


class GroupMessageEvent(MessageEvent):
    """群消息"""
    __event__ = "message.group"
    message_type: Literal["group"]
    sub_type: Literal["normal", "anonymous", "notice"]
    group_id: int
    anonymous: Optional[Anonymous] = None


# Notice Events
class NoticeEvent(Event):
    """通知事件"""
    __event__ = "notice"
    post_type: Literal["notice"]
    notice_type: str


class GroupUploadNoticeEvent(NoticeEvent):
    """群文件上传事件"""
    __event__ = "notice.group_upload"
    notice_type: Literal["group_upload"]
    group_id: int
    user_id: int
    file: File


class GroupAdminNoticeEvent(NoticeEvent):
    """群管理员变动"""
    __event__ = "notice.group_admin"
    notice_type: Literal["group_admin"]
    sub_type: Literal["set", "unset"]
    group_id: int
    user_id: int


class GroupDecreaseNoticeEvent(NoticeEvent):
    """群成员减少事件"""
    __event__ = "notice.group_decrease"
    notice_type: Literal["group_decrease"]
    sub_type: Literal["leave", "kick", "kick_me"]
    group_id: int
    operator_id: int
    user_id: int


class GroupIncreaseNoticeEvent(NoticeEvent):
    """群成员增加事件"""
    __event__ = "notice.group_increase"
    notice_type: Literal["group_increase"]
    sub_type: Literal["approve", "invite"]
    group_id: int
    operator_id: int
    user_id: int


class GroupBanNoticeEvent(NoticeEvent):
    """群禁言事件"""
    __event__ = "notice.group_ban"
    notice_type: Literal["group_ban"]
    sub_type: Literal["ban", "lift_ban"]
    group_id: int
    operator_id: int
    user_id: int
    duration: int


class FriendAddNoticeEvent(NoticeEvent):
    """好友添加事件"""
    __event__ = "notice.friend_add"
    notice_type: Literal["friend_add"]
    user_id: int


class GroupRecallNoticeEvent(NoticeEvent):
    """群消息撤回事件"""
    __event__ = "notice.group_recall"
    notice_type: Literal["group_recall"]
    group_id: int
    user_id: int
    operator_id: int
    message_id: int


class FriendRecallNoticeEvent(NoticeEvent):
    """好友消息撤回事件"""
    __event__ = "notice.friend_recall"
    notice_type: Literal["friend_recall"]
    user_id: int
    message_id: int


class NotifyEvent(NoticeEvent):
    """提醒事件"""
    __event__ = "notice.notify"
    notice_type: Literal["notify"]
    sub_type: str
    user_id: int


class FriendPokeNotifyEvent(NotifyEvent):
    """好友戳一戳提醒事件"""
    __event__ = "notice.notify.poke"
    sub_type: Literal["poke"]
    sender_id: int
    target_id: int


class GroupPokeNotifyEvent(NotifyEvent):
    """群内戳一戳提醒事件"""
    __event__ = "notice.notify.poke"
    sub_type: Literal["poke"]
    group_id: int
    target_id: int


class LuckyKingNotifyEvent(NotifyEvent):
    """群红包运气王提醒事件"""
    __event__ = "notice.notify.lucky_king"
    sub_type: Literal["lucky_king"]
    group_id: int
    target_id: int


class HonorNotifyEvent(NotifyEvent):
    """群荣誉变更提醒事件"""
    __event__ = "notice.notify.honor"
    sub_type: Literal["honor"]
    group_id: int
    honor_type: Literal["talkative:龙王", "performer:群聊之火", "emotion:快乐源泉"]


class GroupCardNoticeEvent(NoticeEvent):
    """群成员名片更新事件"""
    __event__ = "notice.group_card"
    notice_type: Literal["group_card"]
    group_id: int
    user_id: int
    card_new: str
    card_old: str


class OfflineFileNoticeEvent(NoticeEvent):
    """接收到离线文件事件"""
    __event__ = "notice.offline_file"
    notice_type: Literal["offline_file"]
    user_id: int
    file: File


class ClientStatusNoticeEvent(NoticeEvent):
    """其他客户端在线状态变更事件"""
    __event__ = "notice.client_status"
    notice_type: Literal["client_status"]
    client: Device
    online: bool


class EssenceMessageNoticeEvent(NoticeEvent):
    """精华消息事件"""
    __event__ = "notice.essence"
    notice_type: Literal["essence"]
    sub_type: Literal["add", "delete"]
    sender_id: int
    operator_id: int
    message_id: int


# Request Events
class RequestEvent(Event):
    """请求事件"""
    __event__ = "request"
    post_type: Literal["request"]
    request_type: str


class FriendRequestEvent(RequestEvent):
    """加好友请求事件"""
    __event__ = "request.friend"
    request_type: Literal["friend"]
    user_id: int
    comment: str
    flag: str


class GroupRequestEvent(RequestEvent):
    """加群请求/邀请事件"""
    __event__ = "request.group"
    request_type: Literal["group"]
    sub_type: Literal["add", "invite"]
    group_id: int
    user_id: int
    comment: str
    flag: str


# Meta Events
class MetaEvent(Event):
    """元事件"""
    __event__ = "meta_event"
    post_type: Literal["meta_event"]
    meta_event_type: str


class LifecycleMetaEvent(MetaEvent):
    """生命周期元事件"""
    __event__ = "meta_event.lifecycle"
    meta_event_type: Literal["lifecycle"]
    sub_type: str


class HeartbeatMetaEvent(MetaEvent):
    """心跳元事件"""
    __event__ = "meta_event.heartbeat"
    meta_event_type: Literal["heartbeat"]
    status: Status
    interval: int


#Find Event
_trie = StringTrie(separator=".")
for eventmodel in list(globals().values()):
    if inspect.isclass(eventmodel) and issubclass(eventmodel, Event):
        _trie["." + eventmodel.__event__] = eventmodel


def get_event_model(event_name:str) -> List[Type[Event]]:
    #[::-1] ： 把列表倒着弄
    return [model.value for model in _trie.prefixes("." + event_name)][::-1]