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
from F1.PeriodLoader import PeriodLoader
import F3.EventDeliverer as EventDeliverer
from F4.APIParamsGetter import APIParamsGetter

'''
    ws_url='http://127.0.0.1:6700/event'
    ws_url2='http://127.0.0.1:6700/api'
    qqid='643681265'
    cmd_loader_base_path = 'F5/'
'''

class Bot:
    def __init__(self, ws_url:str, ws_url2:str, qqid:str, cmd_loader_base_path:str ,period_loader_path:str, chromedrive_path:str):
        """
        构造Bot对象，用于启动事件循环接受事件。

        :param ws_url: go-cqhttp 服务端 WebSocket 的事件接收域名，端口默认是6700，终结点默认是/event， 默认是http://127.0.0.1:6700/event
        :param ws_url2: go-cqhttp 服务端 WebSocket 的API调用域名，端口默认是6700，终结点默认是/api，默认是http://127.0.0.1:6700/api
        :param qqid: Bot 的 QQ 号，用于判断消息事件是否 at 了自己
        """
        self.ses = aiohttp.ClientSession()
        self.cmd_loader = CommandLoader(cmd_loader_base_path)
        self.period_loader = PeriodLoader(period_loader_path)
        self.ws_url = ws_url
        self.ws_url2 = ws_url2
        self.qqid = qqid
        self.chromedrive_path = chromedrive_path

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

    async def start_callback(self):
        """
        启动Bot回调，目前只是硬编码地发送一句话。

        :return:
        """
        res = await APIParamsGetter.get_send_apiparams_by_user_id(
            message=Message.init_with_segments(MessageSegment.text("bot_44 准备就绪.")),
            user_id=1041159637,
            bot=self
        )

        res2 = await APIParamsGetter.get_send_apiparams_by_group_id(
            message=Message.init_with_segments(MessageSegment.text("bot_44 准备就绪.")),
            group_id=491959457,
            bot=self
        )

        await self.call_api(res)
        await self.call_api(res2)

    async def receiver_loop(self):
        """
        事件循环，开始不断监听Event。

        :return:
        """
        logging.info("(F1.Bot, receiver_loop) Bot receiver_loop started.")
        async for msg in self.ws1:
            if msg.type == aiohttp.WSMsgType.TEXT:
                j=json.loads(msg.data)
                # 获取event
                event = await self.__json_to_event(j)
                if event.post_type != 'meta_event':
                    logging.debug("Received event.")
                    logging.debug(msg.data)
                # Event转交给F3层处理
                try:
                    res = await EventDeliverer.EventDeliverer.handle_event(event, bot=self)
                    await self.call_api(res)
                    # 得到F3层的APIParams返回值，选择调用API
                except Exception as e:
                    logging.error("(F1.Bot, receiver_loop) Exception occurred during trying to handle event.", exc_info=True)

    async def enter_loop(self):
        """
        启动监听事件循环（启动bot的入口）

        :return:
        """

        self.ws1 = await self.ses.ws_connect(self.ws_url)
        self.ws2 = await self.ses.ws_connect(self.ws_url2)
        logging.info("(F1.Bot, enter_loop) Bot successfully created ws1 and ws2.")
        # self.receiver_future = asyncio.create_task(self.receiver_loop())
        await self.start_callback()

        period_task = asyncio.create_task(self.period_loop())
        await self.receiver_loop()
        await period_task #? ： 这个其实在bot被强制关闭前没啥用，因为上一句话的await始终阻塞
        # logging.info("(F1.Bot) Bot successfully created receiver task.")

    async def close(self):
        """
        关闭事件循环，这个函数目前没用

        :return:
        """

        # self.receiver_future.cancel()
        await self.ws1.close()
        await self.ws2.close()
        logging.info("(F1.Bot) Bot successfully closed.")

    async def period_loop(self):
        logging.info("(F1.Bot, period_loop) Start period_loop.")
        coro_tasks_ls = []
        for cls in self.period_loader.class_dict.values():
            inst = await cls.create()
            coro_tasks_ls.append(asyncio.create_task(inst.enter_loop(bot=self)))

        logging.info(f"(F1.Bot, period_loop) Period_loop tasks created. coro_tasks_ls: {coro_tasks_ls}")


if __name__ == '__main__':
    pass