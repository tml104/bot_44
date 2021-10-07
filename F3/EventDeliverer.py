import json

from pydantic import BaseModel
from typing import *

import asyncio
import aiohttp
import logging
import traceback

# import F1.Bot as Bot
import F2.APIParams as APIParams
import F2.Event as Event
import F2.Message as Message
import F4.MessageEventHandler as MessageEventHandler


class EventDeliverer:

    @staticmethod
    async def deliver_message_event(event: Event.MessageEvent, *, bot) -> APIParams.APIParams:
        """
        提取MessageEvent中的Message，然后连同Message、Event、bot一起传入F4层做处理

        :param event:
        :param bot:
        :return:
        """

        try:
            res = await MessageEventHandler.MessageEventHandler.handle_message_event(
                event.message,
                event,
                bot=bot
            )
        except Exception as e:
            from F4.APIParamsGetter import APIParamsGetter
            res = await APIParamsGetter.get_send_apiparams(
                Message.Message.init_with_segments(
                    Message.MessageSegment.text("（F3.EventDeliverer, deliver_message_event）消息事件处理错误：尝试处理事件时遇到了异常.\n"),
                    Message.MessageSegment.text(traceback.format_exc())
                ),
                event,
                bot=bot
            )

        return res

    @staticmethod
    async def deliver_notice_event(event: Event.NoticeEvent, *, bot) -> APIParams.APIParams:
        ...

    @staticmethod
    async def deliver_request_event(event: Event.RequestEvent, *, bot) -> APIParams.APIParams:
        ...

    @staticmethod
    async def deliver_meta_event(event: Event.MetaEvent, *, bot) -> APIParams.APIParams:
        ...

    @staticmethod
    async def handle_event(event: Event.Event, *, bot) -> APIParams.APIParams:
        res = None
        if isinstance(event, Event.MessageEvent):
            res = await EventDeliverer.deliver_message_event(event, bot=bot)
        #     其他event类型有待实现...

        return res
