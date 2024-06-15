import datetime
from .models import SessionLocal, VacancyCount


def save_vacancy_count(count):
    """
    Saves the number of vacancies to the database.

    :param count: Number of vacancies.
    """

    session = SessionLocal()
    try:
        last_record = session.query(VacancyCount).order_by(VacancyCount.datetime.desc()).first()
        changes = count - last_record.count if last_record else 0
        vacancy_count = VacancyCount(count=count,
                                     datetime=datetime.datetime.now(datetime.UTC),
                                     change=changes)
        session.add(vacancy_count)
        session.commit()
    finally:
        session.close()
