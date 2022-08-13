import asyncio
import random
import nonebot
import requests
from nonebot import require, get_bot, get_driver
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment, escape, Bot, Event


try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except BaseException:
    scheduler = None

logger.opt(colors=True).info(
    "已检测到软依赖<y>nonebot_plugin_apscheduler</y>, <g>开启定时任务功能</g>"
    if scheduler
    else "未检测到软依赖<y>nonebot_plugin_apscheduler</y>，<r>禁用定时任务功能</r>"
)

try:
    fire_user_id = get_driver().config.fire_user_id
except Exception as e:
    logger.error("ValueError:{}", e)
    logger.error("请配置fire_user_id")


async def fire_scheduler():
    sendSuccess = False
    while not sendSuccess:
        try:
            await asyncio.sleep(random.randint(1, 3))
            URL = "https://api.qqsuu.cn/api/60s"

            r = requests.get(URL)

            image = r.content

            with open('1.jpg','wb') as f:
             f.write(image)

            await nonebot.get_bot().send_group_msg(group_id=fire_user_id,message=MessageSegment.image('file:///F:/qqbot/60s/1.jpg'))  # 当未连接到onebot.v11协议端时会抛出异常
            logger.info("发送成功")
            sendSuccess = True
        except ValueError as e:
            logger.error("ValueError:{}", e)
            logger.error("发送失败，1s后重试")
            await asyncio.sleep(1)  # 重试前时延，防止阻塞


if scheduler:
    scheduler.add_job(fire_scheduler, "cron", hour="19",minute="24",id="fire_scheduler")