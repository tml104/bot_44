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


import requests as rq
from selenium import webdriver


async def 牌理(regular_message: Message.Message, event:Event.MessageEvent, *, bot) -> Message.Message:
    """
        返回由天凤计算的听牌结果（https://tenhou.net/2/?q={...}）

        格式举例： 牌理 1230m4560s7890p15z 🀇🀈🀉🀋🀓🀔🀕🀔🀟🀠🀡🀝🀀🀆
            - m=萬子, p=筒子, s=索子, z=字牌（1~7：东南西北白发中）, 0=赤
            - 输入的牌的数量是(n*3+2)张时，将显示切牌后的听牌数量；
            - 输入的牌的数量是(n*3+1)张时，将随机发一张牌并显示切牌后的听牌数量；
        
    """
    subcmd = regular_message[1].data['text']

    #preprocess
    def preprocess_pai(subcmd: str):
        ans = ""
        last = 0
        for i,v in enumerate(subcmd):
            if v in "mspz":
                ans += v.join(subcmd[last:i]) + v
                last = i+1
        return ans

    subcmd = preprocess_pai(subcmd)

    url = f"https://tenhou.net/2/?q={subcmd}"
    chromedrive_path = bot.chromedrive_path
    driver = webdriver.Chrome(executable_path=chromedrive_path)
    driver.get(url)

    await asyncio.sleep(2)

    def process_ans_to_unicode(ans: str):
        mp = {
            '1m': '🀇',
            '2m': '🀈',
            '3m': '🀉',
            '4m': '🀊',
            '5m': '🀋',
            '6m': '🀌',
            '7m': '🀍',
            '8m': '🀎',
            '9m': '🀏',

            '1s': '🀐',
            '2s': '🀑',
            '3s': '🀒',
            '4s': '🀓',
            '5s': '🀔',
            '6s': '🀕',
            '7s': '🀖',
            '8s': '🀗',
            '9s': '🀘',

            '1p': '🀙',
            '2p': '🀚',
            '3p': '🀛',
            '4p': '🀜',
            '5p': '🀝',
            '6p': '🀞',
            '7p': '🀟',
            '8p': '🀠',
            '9p': '🀡',

            '1z': '🀀',
            '2z': '🀁',
            '3z': '🀂',
            '4z': '🀃',
            '5z': '🀆',
            '6z': '🀅',
            '7z': '🀄',

            '0m': '🀋',
            '0s': '🀔',
            '0p': '🀝',
        }

        for k,v in mp.items():
            ans = ans.replace(k,v)

        return ans
        
    
    ans = driver.find_element_by_tag_name("textarea").text
    ans = process_ans_to_unicode(ans)
    ans = driver.find_element_by_id("tehai").text + '\n' + ans

    driver.quit()

    return Message.Message.init_with_segments(
        Message.MessageSegment.text(str(ans))
    )