import json

from pydantic import BaseModel
from typing import *

import asyncio
import aiohttp
import logging
import traceback

import re
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

from F6._BasePeriod import _BasePeriod
from F2.Message import Message,MessageSegment
from F4.APIParamsGetter import APIParamsGetter


class _SolidotItem(BaseModel):
    title: str
    link: str
    description: str
    pubdate: str
    sid: int


class SolidotSpider(_BasePeriod):
    url = "https://www.solidot.org/index.rss"
    repeat_time = 1200
    item_dict : Dict[int, _SolidotItem]

    @classmethod
    async def create(cls):
        logging.info("(F6.SolidotSpider, create) create instance started.")
        self = SolidotSpider()
        # self.item_dict = await cls.get_items_dict()
        self.item_dict = {}
        logging.info("(F6.SolidotSpider) create instance ended.")
        return self

    @staticmethod
    def _process_cdata_string(cdata: str) -> str:
        def _remove_link(matchobj: re.Match) -> str:
            # url = matchobj.group(1)
            content_str = matchobj.group(2)
            return f"{content_str}"

        p = re.compile(r"<a href=\"(.*?)\">(.*?)</a>")
        return p.sub(_remove_link, cdata)

    @staticmethod
    def _get_sid_from_link(link: str) -> int:
        n = re.search(r"sid=([0-9]*)", link).group(1)
        return int(n)

    @staticmethod
    async def get_items_dict():
        logging.info("(F6.SolidotSpider, get_items_dict) get_items_dict started.")
        d = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(SolidotSpider.url) as resp:
                # print("Status:", resp.status)
                resp_text = await resp.text()

        logging.info("(F6.SolidotSpider, get_items_dict) resp_text got.")

        soup = BeautifulSoup(resp_text, "xml", parse_only=SoupStrainer("item"))
        item_ls = soup.find_all("item")
        for item in item_ls:
            title = SolidotSpider._process_cdata_string(item.title.string)
            description = SolidotSpider._process_cdata_string(item.description.string)
            link = SolidotSpider._process_cdata_string(item.link.string)
            pubdate = SolidotSpider._process_cdata_string(item.pubDate.string)
            sid = SolidotSpider._get_sid_from_link(link)
            d[sid] = _SolidotItem(
                title=title,
                description=description,
                link=link,
                pubdate=pubdate,
                sid=sid
            )

        logging.info("(F6.SolidotSpider, get_items_dict) d processed.")

        return d

    @staticmethod
    def get_message_by_item(item: _SolidotItem) -> Message:
        # return Message.init_with_segments(
        #     MessageSegment.text(item.title),
        #     MessageSegment.text('\n\n'),
        #     MessageSegment.text(item.pubdate+'\n'),
        #     MessageSegment.text(item.link),
        #     MessageSegment.text('\n\n'),
        #     MessageSegment.text(item.description),
        #     MessageSegment.text('\n\n'),
        #     MessageSegment.text("(来源：Solidot)")
        # )
        return Message.init_with_segments(
            MessageSegment.text(
                item.title + '\n\n' + item.pubdate + '\n' + item.link + '\n\n' + item.description + '\n\n'
                + "(来源：Solidot)"
            )
        )

    def get_diff_items_dict(self, d2: dict):
        nd = {}
        for k,v in d2.items():
            if k not in self.item_dict:
                nd[k] = v
        return nd

    async def main(self, *, bot):
        nd = await self.get_items_dict()
        diff_dict = self.get_diff_items_dict(nd)
        for k,v in diff_dict.items():
            await bot.call_api(await APIParamsGetter.get_send_apiparams_by_user_id(
                message=self.get_message_by_item(v),
                user_id=1041159637,
                bot=bot
            ))
            await asyncio.sleep(5)
        self.item_dict.update(diff_dict)

    async def enter_loop(self, *, bot):
        while True:
            await self.main(bot=bot)
            logging.info(f"(F6.SolidotSpider, enter_loop) Main done, start to wait for {self.repeat_time} sec.")
            await asyncio.sleep(self.repeat_time)


