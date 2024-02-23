from discord.ext import commands

def add_command(bot, name=None):
    def decorator(func):
        nonlocal name
        if name is None:
            name = func.__name__
        bot.add_command(commands.Command(func, name=name))
        return func
    return decorator
