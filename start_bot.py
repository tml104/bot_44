import F1.Bot as Bot
import aiohttp
import asyncio
import logging
import configparser

if __name__ == '__main__':
    logging.basicConfig(filename='./log.txt', format="%(levelname)s , %(asctime)s: %(message)s", level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read('config.cfg')
    config_dict = config['DEFAULT']

    ws_url = config_dict['ws_url']
    ws_url2 = config_dict['ws_url2']
    qqid = config_dict['qqid']
    cmd_loader_base_path = config_dict['cmd_loader_base_path']
    period_loader_path = config_dict['period_loader_path']
    chromedrive_path = config_dict['chromedrive_path']
    logging.info(f"config args: {ws_url}, {ws_url2}, {qqid}, {cmd_loader_base_path}")

    bot = Bot.Bot(
        ws_url,
        ws_url2,
        qqid,
        cmd_loader_base_path,
        period_loader_path,
        chromedrive_path
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.enter_loop())
    # print("run_until_complete finished")
    # loop.close()