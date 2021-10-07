import json

from pydantic import BaseModel

import asyncio
import aiohttp
import logging

# import F1.Bot as Bot
import F2.APIParams as APIParams
import F2.Event as Event
import F2.Message as Message

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

