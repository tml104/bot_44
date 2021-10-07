import json

from pydantic import BaseModel
from typing import *

import asyncio
import aiohttp
import importlib
import os.path
import logging
import inspect

from F2.Message import Message, MessageSegment
from F2.Event import *
from F2.APIParams import *


class CommandLoader:
    """
        装有命令名称到命令的字典，扫描F5层下的所有模块来实现
        command_dict : Dict[str, fun]
    """
    base_path = 'F5/'

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.command_dict = self.load_commands()

    def load_commands(self):
        logging.info("(F1.CommandLoader, load_commands) CommandLoader load started.")
        d = {}
        for module_file in os.listdir(self.base_path):
            # 去除后缀
            module_name = os.path.splitext(module_file)[0]
            # 排除目录
            if os.path.isdir(os.path.join(self.base_path, module_name)):
                continue

            module = importlib.import_module(self.base_path.replace('/','.') + module_name)
            # d.update({x:y for x,y in module.__dict__.items() if x[:1]!='_' and inspect.isfunction(y)})
            d.update(inspect.getmembers(module, inspect.isfunction))

        logging.info(f"(F1.CommandLoader, load_commands) CommandLoader load finished. {len(d)} command(s) were loaded.")
        logging.info(f"(F1.CommandLoader, load_commands) d: {d}")
        return d

    def reload(self):
        self.command_dict = CommandLoader.load_commands()