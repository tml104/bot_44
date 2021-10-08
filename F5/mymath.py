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
import math


async def isprime(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        判断一个数是否是质数。

        格式：isprime arg1
            arg1: 要判断的数
    """
    n = int(regular_message[1].data['text'])

    return Message.Message.init_with_segments(
        Message.MessageSegment.text("isprime: True" if sympy.isprime(n) else "isprime: False")
    )


async def gcd(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        最大公因数。

        格式：gcd x y
            x, y: 要求的数
    """
    x = int(regular_message[1].data['text'])
    y = int(regular_message[2].data['text'])
    ans = math.gcd(x, y)

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )


async def lcm(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        最小公倍数。

        格式：lcm x y
            x, y: 要求的数
    """
    x = int(regular_message[1].data['text'])
    y = int(regular_message[2].data['text'])
    ans = sympy.lcm(x, y)

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )


async def log(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        对数。

        格式：log b x  (or) log x
            b: 基
            x: 要求的数
    """
    x = float(regular_message[1].data['text'])
    if len(regular_message) == 3:
        y = float(regular_message[2].data['text'])
        ans = math.log(y, x)
    else:
        ans = math.log(x)

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )


async def sqrt(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        开方。

        格式：sqrt x
            x: 要求的数
    """
    x = float(regular_message[1].data['text'])
    ans = math.sqrt(x)

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )


async def sin(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        三角函数sin。

        格式：sin x
            x: 要求的数
    """
    x = float(regular_message[1].data['text'])
    ans = math.sin(x)

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )


async def cos(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        三角函数cos。

        格式：cos x
            x: 要求的数
    """
    x = float(regular_message[1].data['text'])
    ans = math.cos(x)

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )


async def tan(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        三角函数tan。

        格式：tan x
            x: 要求的数
    """
    x = float(regular_message[1].data['text'])
    ans = math.tan(x)

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )