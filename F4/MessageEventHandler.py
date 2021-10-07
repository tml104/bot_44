import json

from pydantic import BaseModel
from typing import *

import asyncio
import aiohttp
import logging

# import F1.Bot as Bot
import F2.APIParams as APIParams
import F2.Event as Event
import F2.Message as Message
from F4.APIParamsGetter import APIParamsGetter


class MessageEventHandler:

    @staticmethod
    async def convert_to_regular_message(message: Message.Message) -> Message.Message:
        """
        将普通消息分段，分成参数形式的message

        :param message:
        :return:
        """

        # 将普通消息分段，分成参数形式的message
        regular_message = list()

        for i, v in enumerate(message):

            v: Message.MessageSegment

            # 纯文本消息段
            if v.type == 'text':
                tx: str = v.data['text']
                tx_ls = tx.strip().split()
                for x in tx_ls:
                    if x.isspace(): continue
                    regular_message.append(Message.MessageSegment.text(x))
            # 非纯文本消息段屏蔽at，其他的原封不动
            elif v.type == 'at':
                continue
            else:
                regular_message.append(v)

        return Message.Message.parse_obj(regular_message)

    @staticmethod
    async def handle_message_as_command(message: Message.Message, event: Event.MessageEvent, *,
                                        bot) -> APIParams.APIParams:
        """
        把message当作命令处理。从这里开始实现真正的命令处理逻辑。
        主要操作是：message是一个message segment列表，先扫一遍该列表，查找是否在开头at了me，如果是，那么将message转化为regular message，
        转化完成后，去F5层寻找对应函数调用（如果能找到，那么就传入regular message，event和bot），接受返回值（也是message），最后根据event类型构造灰顶APIParams返回。

        :param message:
        :param event:
        :param bot:
        :return:
        """
        logging.info("(F4.MessageEventHandler, handle_message_as_command) Start Handling of MessageEvent as command.")

        # 判断message的第一个messagesegment是否是在at自己
        first_message_segment = message[0]
        at_me_flag = False
        # 是at自己的
        if first_message_segment.type == 'at' and first_message_segment.data['qq'] == bot.qqid:
            at_me_flag = True

        logging.info(f"(F4.MessageEventHandler, handle_message_as_command) at_me_flag == {at_me_flag}.")

        # message中有at me，触发指令判断
        if at_me_flag:
            # 取得regular_message
            regular_message = await MessageEventHandler.convert_to_regular_message(message)

            # 寻找对应函数调用
            # 首个消息段不是text
            if regular_message[0].type != 'text':
                logging.info("(F4.MessageEventHandler, handle_message_as_command) Command Params error: Message not "
                             "starts from text.")
                return await APIParamsGetter.get_send_apiparams(
                    Message.Message.init_with_segments(Message.MessageSegment.text("(F4.MessageEventHandler, handle_message_as_command) 参数错误：消息起始段不是文本.")),
                    event,
                    bot=bot
                )
            # 取得命令名字
            command_name = regular_message[0].data['text']
            # 取得对应异步函数
            fun = bot.cmd_loader.command_dict.get(command_name)
            # 找不到对应命令名字的函数
            if fun is None:
                logging.info("(F4.MessageEventHandler, handle_message_as_command) Command not found.")
                return await APIParamsGetter.get_send_apiparams(
                    Message.Message.init_with_segments(Message.MessageSegment.text("(F4.MessageEventHandler, handle_message_as_command) 命令错误：找不到对应命令.")),
                    event,
                    bot=bot
                )
            # 否则能找到，用await调用之，返回一个message
            logging.info(f"(F4.MessageEventHandler, handle_message_as_command) Command found, name is {command_name}.")
            msg = await fun(regular_message, event, bot=bot)
            # 返回对应apiparams
            return await APIParamsGetter.get_send_apiparams(
                msg,
                event,
                bot=bot
            )

    @staticmethod
    async def handle_message_event(message: Message.Message, event: Event.MessageEvent, *,
                                   bot) -> APIParams.APIParams:
        """
        入口

        :param message:
        :param event:
        :param bot:
        :return:
        """
        return await MessageEventHandler.handle_message_as_command(message, event, bot=bot)
