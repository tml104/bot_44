import json

from pydantic import BaseModel

import asyncio
import aiohttp
import logging

# import F1.Bot as Bot
import F2.APIParams as APIParams
import F2.Event as Event
import F2.Message as Message
import utils.utils as utils

import sympy


async def h(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        显示所有命令的帮助信息。
    """
    d:dict = bot.cmd_loader.command_dict
    return Message.Message.init_with_segments(*[
        Message.MessageSegment.text(f"{fun_name}: {fun.__doc__}\n") for fun_name, fun in d.items()
    ])


async def hey(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        使Bot回复一段颜文字。
    """
    return Message.Message.init_with_segments(
        Message.MessageSegment.text("ヽ(✿ﾟ▽ﾟ)ノ")
    )


async def isprime(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        判断一个数是否是质数。
    """
    n = int(regular_message[1].data['text'])

    return Message.Message.init_with_segments(
        Message.MessageSegment.text("isprime: True" if sympy.isprime(n) else "isprime: False")
    )


async def solidot(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        订阅来自 Solidot 的新闻。

        子命令：
        solidot enable/disable: 启用或禁用该功能
        solidot DY: 将当前群/用户加入订阅列表
        solidot TD: 将当前群/用户移除订阅列表
        solidot list: 列出所有正在订阅的群/用户
    """
    subcmd = regular_message[1].data['text']

    solidot_spider, std = utils.get_settings("SolidotSpider")
    res = ""
    change_flag = False
    group_list = utils.get_settings("SolidotSpider", "group_list", std=std)[0]
    user_list = utils.get_settings("SolidotSpider", "user_list", std=std)[0]

    if subcmd == "enable":
        solidot_spider["enable"] = True
        change_flag = True
        res = "Solidot 功能开启."
    elif subcmd == "enable":
        solidot_spider["enable"] = False
        change_flag = True
        res = "Solidot 功能关闭."
    elif subcmd == "list":
        res = "订阅 Solidot 的群与用户: \n"
        group_list_str = "群：" + " ".join(map(str, group_list))
        user_list_str = "用户：" + " ".join(map(str, user_list))
        res += group_list_str + '\n' + user_list_str + '\n'
    elif subcmd == "DY":
        change_flag = True
        if isinstance(event, Event.GroupMessageEvent):
            if event.group_id not in group_list:
                group_list.append(event.group_id)
            res = f"订阅群号:{event.group_id}"
        elif isinstance(event, Event.PrivateMessageEvent):
            if event.user_id not in user_list:
                user_list.append(event.user_id)
            res = f"订阅用户:{event.user_id}"
    elif subcmd == "TD":
        change_flag = True
        if isinstance(event, Event.GroupMessageEvent):
            if event.group_id in group_list:
                group_list.remove(event.group_id)
            res = f"退订群号:{event.group_id}"
        elif isinstance(event, Event.PrivateMessageEvent):
            if event.user_id in user_list:
                user_list.remove(event.user_id)
            res = f"退订用户:{event.user_id}"

    if change_flag:
        json.dump(std, open("./settings.json", "w"))

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(res)
    )