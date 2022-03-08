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
from F6._BasePeriod import _BasePeriod


class PeriodLoader:
    """
        装有类名称到类的字典，扫描F6层下的所有模块来实现
        command_dict : Dict[str, fun]
    """
    base_path = 'F6/'
    class_dict: Dict[str, Type[_BasePeriod]]

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.class_dict = self.load_classes()

    def load_classes(self):
        """
            将base path下的所有模块装入字典中，返回该字典
        """
        logging.info("(F1.PeriodLoader, load_classes) PeriodLoader load started.")
        d = {}
        for module_file in os.listdir(self.base_path):
            # 去除后缀
            module_name = os.path.splitext(module_file)[0]
            logging.debug(f"(F1.PeriodLoader, load_classes) module_name: {module_name}")
            # 排除目录
            if os.path.isdir(os.path.join(self.base_path, module_name)) or module_name[0] == '_':
                continue

            module = importlib.import_module(self.base_path.replace('/', '.') + module_name)
            # d.update(inspect.getmembers(module, inspect.isfunction))
            logging.debug(f"(F1.PeriodLoader, load_classes) module: {module}")
            d.update(inspect.getmembers(module, lambda obj: inspect.isclass(obj) and (obj is not _BasePeriod) and issubclass(obj, _BasePeriod)))

        logging.info(
            f"(F1.PeriodLoader, load_classes) PeriodLoader load finished. {len(d)} class(es) were loaded.")
        logging.info(f"(F1.PeriodLoader, load_classes) d: {d}")
        return d

    def reload(self):
        self.class_dict = self.load_classes()


'''
import F6.SolidotSpider
from F6._BasePeriod import _BasePeriod
import inspect
inspect.getmembers(F6.SolidotSpider, lambda obj: inspect.isclass(obj) and issubclass(obj, _BasePeriod) and obj is not _BasePeriod)
'''