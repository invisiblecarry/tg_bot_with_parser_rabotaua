from aiogram import Bot
from aiogram.types import BotCommand
from config_data.config import Config


async def set_default_commands(bot: Bot):
    """
    Sets the default commands for the Telegram bot.
    This function initializes the default commands for the bot based on the configuration provided.
    :param bot: Instance of the Telegram bot.
    """
    commands = [BotCommand(command=command, description=description)
                for command, description in Config.DEFAULT_COMMANDS]
    await bot.set_my_commands(commands)
