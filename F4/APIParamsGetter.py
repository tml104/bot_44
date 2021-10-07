import asyncio
import aiohttp
import logging

import F2.APIParams as APIParams
import F2.Event as Event
import F2.Message as Message


class APIParamsGetter:
    @staticmethod
    async def get_send_apiparams(message: Message.Message, event: Event.MessageEvent, *,
                                 bot) -> APIParams.APIParams:
        '''
        根据event，发送回复，这个函数将返回对应的APIParams。

        :param message:
        :param event:
        :param bot:
        :return:
        '''

        user_id = event.user_id
        message_type = event.message_type

        if message_type == 'private':
            return APIParams.SendPrivateMsg(user_id=user_id, message=message)
        elif message_type == 'group':
            if not isinstance(event, Event.GroupMessageEvent):
                raise ValueError("event is not Event.GroupMessageEvent.")
            group_id = event.group_id
            return APIParams.SendGroupMsg(group_id=group_id, message=message)

    @staticmethod
    async def get_send_apiparams_by_group_id(message: Message.Message, group_id:int, *, bot) -> APIParams.APIParams:
        return APIParams.SendGroupMsg(group_id=group_id, message=message)

    @staticmethod
    async def get_send_apiparams_by_user_id(message: Message.Message, user_id:int, *, bot) -> APIParams.APIParams:
        return APIParams.SendPrivateMsg(user_id=user_id, message=message)