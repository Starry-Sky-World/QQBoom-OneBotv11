from nonebot import on_command, require, on_message, on
from nonebot.rule import to_me, is_type
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment, GroupMessageEvent
from nonebot import logger
from nonebot.params import CommandArg, EventPlainText, EventMessage
import asyncio

logger.info("机器人收到任意消息后会启动")

get_message = on_message(priority=1)
Ifuse = False  # 全局变量，用于控制轰炸的状态

@get_message.handle()
async def _(bot: Bot, message: GroupMessageEvent):
    global Ifuse  # 声明 Ifuse 为全局变量
    message_text = message.get_message().extract_plain_text()
    message_userid = message.get_user_id()
    
    if "StartBoom" in message_text:
        await bot.call_api("send_private_msg", user_id=message_userid, message="触发插件：BoomQQ | 请在Console上输入轰炸目标以及信息！")
        logger.info("机器人已发送提示信息")
        logger.info("请在Console上输入轰炸目标以及信息！")
        
        # 输入验证和异常处理逻辑
        try:
            IfGroup = bool(int(input("是否为群聊？（1为是，0为否） > ")))
            if IfGroup:
                group_id = int(input("请输入目标群号 > "))
                message_text = input("请输入要轰炸的信息 > ")
                frequency = int(input("请输入次数 > "))
            else:
                user_id = int(input("请输入目标QQ号 > "))
                message_text = input("请输入要轰炸的信息 > ")
                frequency = int(input("请输入次数 > "))
                
            # 检查频率值
            if frequency <= 0:
                logger.error("轰炸次数必须大于0！")
                return await get_message.finish()

            logger.info(f"输入的轰炸次数: {frequency}")

            Ifuse = True
            
            # 异步发送消息
            async def send_messages():
                if IfGroup:
                    tasks = []
                    for i in range(frequency):
                        tasks.append(bot.call_api("send_group_msg", group_id=group_id, message=message_text))
                        logger.info(f"准备发送第 {i + 1} 条群消息")
                    await asyncio.gather(*tasks)  # 并发发送所有消息
                else:
                    tasks = []
                    for i in range(frequency):
                        tasks.append(bot.call_api("send_private_msg", user_id=user_id, message=message_text))
                        logger.info(f"准备发送第 {i + 1} 条私聊消息")
                    await asyncio.gather(*tasks)  # 并发发送所有消息

            await send_messages()  # 调用异步发送消息的函数
            logger.info("机器人已完成轰炸！重启再次使用！")
        
        except ValueError:
            logger.error("输入值无效，请确保输入正确的数字。")
        
        except Exception as e:
            logger.error(f"发生了一个错误: {e}")

    return await get_message.finish()
