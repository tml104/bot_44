import json

from pydantic import BaseModel
from typing import *

import asyncio
import aiohttp
import logging
import traceback

from F2.Message import Message, MessageSegment
import F2.Event as Event
import F2.APIParams as APIParams
from F1.CommandLoader import CommandLoader
import F3.EventDeliverer as EventDeliverer

'''
    ws_url='http://127.0.0.1:6700/event'
    ws_url2='http://127.0.0.1:6700/api'
    qqid='643681265'
    cmd_loader_base_path = 'F5/'
'''

class Bot:
    def __init__(self, ws_url:str, ws_url2:str, qqid:str, cmd_loader_base_path:str):
        """
        构造Bot对象，用于启动事件循环接受事件。

        :param ws_url: go-cqhttp 服务端 WebSocket 的事件接收域名，端口默认是6700，终结点默认是/event， 默认是http://127.0.0.1:6700/event
        :param ws_url2: go-cqhttp 服务端 WebSocket 的API调用域名，端口默认是6700，终结点默认是/api，默认是http://127.0.0.1:6700/api
        :param qqid: Bot 的 QQ 号，用于判断消息事件是否 at 了自己
        """
        self.ses = aiohttp.ClientSession()
        self.cmd_loader = CommandLoader(cmd_loader_base_path)
        self.ws_url = ws_url
        self.ws_url2 = ws_url2
        self.qqid = qqid

    @staticmethod
    async def __json_to_event(j: Dict) -> Event.Event:
        """
        将字典j转化为Event对象。

        :param j: 字典
        :return: Event对象
        """
        post_type = j['post_type']
        detail_type = j.get(f"{post_type}_type")
        detail_type = f".{detail_type}" if detail_type else ""
        sub_type = j.get("sub_type")
        sub_type = f".{sub_type}" if sub_type else ""
        models = Event.get_event_model(post_type + detail_type + sub_type)

        event = None
        for model in models:
            try:
                event = model.parse_obj(j)
                break
            except Exception as e:
                logging.error("Exception in handle_receive_json", exc_info=True)

        return event

    async def call_api(self, apiparams: APIParams.APIParams):
        """
        由 Bot 对象直接调用 API，其将APIParams对象封装为完整的API字典。API字典形如：
        {
            "action":"send_group_msg",
            "params":{
                "group_id":491959457,
                "message":"喵"
            }
        }
        这里接受的参数是"params"中的字典形式。

        :param apiparams: APIParams 对象。
        :return: 无
        """

        if apiparams is None:
            return
        d = {
            "action": apiparams.__apiname__,
            "params": apiparams.dict()
        }

        await self.ws2.send_json(d)

    async def receiver_loop(self):
        """
        事件循环，开始不断监听Event。

        :return:
        """

        async for msg in self.ws1:
            if msg.type == aiohttp.WSMsgType.TEXT:
                logging.debug("Received event.")
                logging.debug(msg.data)
                j=json.loads(msg.data)
                # 获取event
                event = await self.__json_to_event(j)
                # Event转交给F3层处理
                try:
                    res = await EventDeliverer.EventDeliverer.handle_event(event, bot=self)
                    await self.call_api(res)
                    # 得到F3层的APIParams返回值，选择调用API
                except Exception as e:
                    logging.error("(F1.Bot) Exception occurred during trying to handle event.", exc_info=True)

    async def enter_loop(self):
        """
        启动监听事件循环

        :return:
        """

        self.ws1 = await self.ses.ws_connect(self.ws_url)
        self.ws2 = await self.ses.ws_connect(self.ws_url2)
        logging.info("(F1.Bot) Bot successfully created ws1 and ws1.")
        # self.receiver_future = asyncio.create_task(self.receiver_loop())
        await self.receiver_loop()
        # logging.info("(F1.Bot) Bot successfully created receiver task.")

    async def close(self):
        """
        关闭事件循环

        :return:
        """

        self.receiver_future.cancel()
        await self.ws1.close()
        await self.ws2.close()
        logging.info("(F1.Bot) Bot successfully closed.")


if __name__ == '__main__':
    pass