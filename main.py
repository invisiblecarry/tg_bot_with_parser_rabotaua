import asyncio
from database.models import init_db
from parsers.job_parser import fetch_vacancies
from tg_bot.bot import *


async def periodic_fetch_vacancies(interval: int) -> None:
    """
    Periodically fetch vacancies every 'interval' seconds.

    :param interval: Interval in seconds.
    """
    while True:
        fetch_vacancies()
        await asyncio.sleep(interval)


async def main() -> None:
    """
    Running the job parser every hour and the bot asynchronously
    """
    init_db()
    await asyncio.gather(
        periodic_fetch_vacancies(3600),
        bot_main()
    )

if __name__ == '__main__':
    asyncio.run(main())