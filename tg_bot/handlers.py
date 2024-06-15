from aiogram import Router, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import FSInputFile
from database.models import VacancyCount, SessionLocal
import pandas as pd
from datetime import datetime
from parsers.job_parser import fetch_vacancies

router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {message.from_user.full_name}! type '/help' to get a hint")


@router.message(Command(commands=["help"]))
async def send_help(message: types.Message):
    await message.answer(f"Type '/get_today_statistic' to get today statistics on the"
                         f" number of vacancies for the 'Junior' request from the rabota.ua")


@router.message(Command(commands=["get_today_statistic"]))
async def send_statistics(message: types.Message):
    """
    Sends today's statistics to the user as an Excel file.
    :param message: The message object.
    """
    # fetch_vacancies()
    today = datetime.now().date()
    session = SessionLocal()
    try:
        data = session.query(VacancyCount).filter(VacancyCount.datetime >= today).all()
        df = pd.DataFrame([(d.datetime, d.count) for d in data], columns=["datetime", "vacancy_count"])
        df['change'] = df['vacancy_count'].diff().fillna(0).astype(int)
        file_path = "statistics.xlsx"
        df.to_excel(file_path, index=False)

        # using FSInputFile for sending documents
        document = FSInputFile(file_path)
        await message.answer_document(document)
    except Exception as e:
        await message.answer(f"Error fetching statistics: {e}")
    finally:
        session.close()


def register_handlers(dp: Dispatcher):
    """
    Registers command handlers for the Telegram bot.
    :param dp: Dispatcher.
    """
    dp.include_router(router)
