import discord
from discord.ext import commands
from .bot_intents import *


def setup_bot(prefix,intents ):
    """
    創建和設置一個 Discord bot。
    
    :param prefix: 字符串，定義命令的前綴字符。
    :return: 返回一個設置好的 bot 實例。
    """
    
    
    bot = commands.Bot(command_prefix=prefix)
    
   
    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    return bot
