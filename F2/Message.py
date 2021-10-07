from pydantic import BaseModel
from typing import *
from utils.utils import _b2s


class MessageSegment(BaseModel):
    type: str
    data: Optional[Dict[str, Any]]

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment(type="text", data={
            "text": text
        })

    @staticmethod
    def face(face_id: int) -> "MessageSegment":
        return MessageSegment(type="face", data={
            "id": str(face_id)
        })

    @staticmethod
    def record(file: str,
               magic: Optional[bool] = None,
               cache: Optional[bool] = None,
               proxy: Optional[bool] = None,
               timeout: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(
            type="record", data={
                "file": file,
                "magic": _b2s(magic),
                "cache": _b2s(cache),
                "proxy": _b2s(proxy),
                "timeout": timeout
            })

    @staticmethod
    def video(file: str,
              cover: Optional[str] = None,
              c_: int = 1) -> "MessageSegment":
        return MessageSegment(type="video", data={
            "file": file,
            "cover": cover,
            "c_": c_
        })

    @staticmethod
    def at(qq: Union[int, str], name: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(type="at", data={"qq": str(qq), "name": name})

    @staticmethod
    def rps() -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(type="rps", data={})

    @staticmethod
    def dice() -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(type="dice", data={})

    @staticmethod
    def shake() -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(type="shake", data={})

    @staticmethod
    def anonymous(ignore_failure: Optional[bool] = None) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(type="anonymous", data={"ignore": _b2s(ignore_failure)})

    @staticmethod
    def share(url: str = "",
              title: str = "",
              content: Optional[str] = None,
              image: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(type="share", data={
            "url": url,
            "title": title,
            "content": content,
            "image": image
        })

    @staticmethod
    def contact(type_: str, id: int) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(type="contact", data={"type": type_, "id": str(id)})

    @staticmethod
    def contact_group(group_id: int) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(type="contact", data={"type": "group", "id": str(group_id)})

    @staticmethod
    def contact_user(user_id: int) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(type="contact", data={"type": "qq", "id": str(user_id)})

    @staticmethod
    def location(latitude: float,
                 longitude: float,
                 title: Optional[str] = None,
                 content: Optional[str] = None) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(
            type="location", data={
                "lat": str(latitude),
                "lon": str(longitude),
                "title": title,
                "content": content
            })

    @staticmethod
    def music(type_: str, id_: int) -> "MessageSegment":
        return MessageSegment(type="music", data={"type": type_, "id": id_})

    @staticmethod
    def music_custom(url: str,
                     audio: str,
                     title: str,
                     content: Optional[str] = None,
                     image: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            type="music", data={
                "type": "custom",
                "url": url,
                "audio": audio,
                "title": title,
                "content": content,
                "image": image
            })

    @staticmethod
    def image(file: str,
              type_: Optional[Literal["flash", "show"]] = None,
              cache: bool = True,
              id_: int = 40000,
              c_: int = 1) -> "MessageSegment":
        return MessageSegment(
            type="image", data={
                "file": file,
                "type": type_,
                "cache": cache,
                "id_": id_,
                "c_": c_
            })

    @staticmethod
    def reply(id_: int,
              text: Optional[str] = None,
              qq: Optional[int] = None,
              time: Optional[int] = None,
              seq: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(
            type="reply", data={
                "id": str(id_),
                "text": text,
                "qq": str(qq),
                "time": str(time),
                "seq": str(seq)
            })

    @staticmethod
    def poke(qq: Union[int, str]) -> "MessageSegment":
        return MessageSegment(type="poke", data={"qq": str(qq)})

    @staticmethod
    def gift(qq: Union[int, str], id_: Union[int, str]) -> "MessageSegment":
        return MessageSegment(type="poke", data={"qq": str(qq), "id": str(id_)})

    @staticmethod
    def forward(id_: str) -> "MessageSegment":
        # log("WARNING", "Forward Message only can be received!")
        return MessageSegment(type="forward", data={"id": id_})

    @staticmethod
    def node(id_: int,
             name: Optional[str] = None,
             uin: Optional[int] = None,
             content: Optional["MessageSegment"] = None,
             seq: Optional["MessageSegment"] = None) -> "MessageSegment":
        return MessageSegment(
            type="node", data={
                "id": str(id_),
                "name": name,
                "uin": str(uin),
                "content": content,
                "seq": seq
            })

    @staticmethod
    def xml(data: str, resid: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(type="xml", data={"data": data, "resid": resid})

    @staticmethod
    def json(data: str, resid: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(type="json", data={"data": data, "resid": resid})

    @staticmethod
    def cardimage(file: str,
                  minwidth: int = 400,
                  minheight: int = 400,
                  maxwidth: int = 500,
                  maxheight: int = 1000,
                  source: Optional[str] = None,
                  icon: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            type="cardimage", data={
                "file": file,
                "minwidth": str(minwidth),
                "minheight": str(minheight),
                "maxwidth": str(maxwidth),
                "maxheight": str(maxheight),
                "source": source,
                "icon": icon
            })

    @staticmethod
    def tts(text: str) -> "MessageSegment":
        return MessageSegment(type="tts", data={"text": text})


class Message(BaseModel):
    __root__ : List[MessageSegment]

    def __getitem__(self, item):
        return self.__root__[item]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def append(self, item: MessageSegment):
        return self.__root__.append(item)

    @staticmethod
    def init_with_segments(*args, **kwargs) -> "Message":
        return Message.parse_obj(args)


if __name__ == "__main__":
    print(
        Message.init_with_segments(MessageSegment.text("ヽ(✿ﾟ▽ﾟ)ノ"))
    )
