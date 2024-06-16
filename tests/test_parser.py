import unittest
from datetime import datetime
from parsers.job_parser import fetch_vacancies
from database.models import SessionLocal, VacancyCount, init_db


class TestVacancyParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.session = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_fetch_vacancies(self):
        initial_count = self.session.query(VacancyCount).count()
        fetch_vacancies()
        new_count = self.session.query(VacancyCount).count()
        self.assertEqual(new_count, initial_count + 1, "Vacancy count should increase by 1 after fetching vacancies")

    def test_vacancy_count_data(self):
        fetch_vacancies()
        latest_entry = self.session.query(VacancyCount).order_by(VacancyCount.datetime.desc()).first()
        self.assertIsNotNone(latest_entry, "Latest entry should not be None")
        self.assertGreater(latest_entry.count, 0, "The vacancy count should be greater than 0")

    def test_vacancy_count_change(self):
        fetch_vacancies()
        previous_entry = self.session.query(VacancyCount).order_by(VacancyCount.datetime.desc()).offset(1).first()
        latest_entry = self.session.query(VacancyCount).order_by(VacancyCount.datetime.desc()).first()
        if previous_entry:
            self.assertEqual(latest_entry.count - previous_entry.count, latest_entry.change,
                             "Change in vacancy count should be correctly recorded")


if __name__ == '__main__':
    unittest.main()


