from aiogram import Bot, Dispatcher
from config_data.config import Config
from tg_bot.handlers import register_handlers
from utils.set_bot_commands import set_default_commands

# Initialize the bot with the token from the configuration
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)

# Create a Dispatcher instance for handling updates
dp = Dispatcher()

# Register handlers for the Dispatcher
register_handlers(dp)


async def on_startup():
    """
    Function to be executed on bot startup.
    Sets the default commands for the bot and prints a startup message.
    """
    await set_default_commands(bot)
    print('Bot started')


async def bot_main():
    """
    Main function to run the bot.
    Executes startup tasks and starts polling for updates.
    """
    await on_startup()
    await dp.start_polling(bot)

