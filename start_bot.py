import F1.Bot as Bot
import aiohttp
import asyncio
import logging
import configparser

if __name__ == '__main__':
    logging.basicConfig(filename='./log.txt', format="%(levelname)s , %(asctime)s: %(message)s", level=logging.DEBUG)

    bot = Bot.Bot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.enter_loop())
    # print("run_until_complete finished")
    # loop.close()