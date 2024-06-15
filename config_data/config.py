import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Environment variables not loaded because file .env is missing')
else:
    load_dotenv()


class Config:
    """
    Class contains configuration parameters
    """

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    DATABASE_URI = os.getenv('DATABASE_URI')

    ROBOTA_URL = os.getenv('ROBOTA_URL')

    DEFAULT_COMMANDS = [
        ('start', 'Start tg_bot'),
        ('help', 'Display help'),
        ('get_today_statistic', 'Get today statistics')
    ]
