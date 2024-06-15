import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from database.db import save_vacancy_count
from config_data.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
URL = Config.ROBOTA_URL


def fetch_vacancies() -> None:
    """
    Fetch the number of vacancies from the specified URL using Selenium and save the count to the database.
    This function uses Selenium to load the page specified by the URL in the configuration,
    finds the element containing the number of vacancies, extracts this number, and saves it to the database.
    :return: None
    """
    url = URL
    logger.info(f'Fetching vacancies from {url}')
    # selenium settings
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # chrome diver set up
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        driver.implicitly_wait(10)  # waiting for content to load

        # find the element that contains the job count using XPath
        vacancies_header = driver.find_element(By.XPATH,
                                               "//*[contains(text(),'вакансий') or"
                                               " contains(text(),'вакансия') or "
                                               "contains(text(),'вакансии')]")

        if not vacancies_header:
            logger.error('Vacancies header count element not found')
            return

        try:
            text = vacancies_header.text.strip()
            logger.info(f'Vacancies header text: "{text}"')
            count = int(
                text.replace('вакансий', '').
                replace('вакансии', '').
                replace('вакансия', '').
                replace(' ', '').
                strip())
            logger.info(f'Found {count} vacancies')

            # saving to database
            save_vacancy_count(count)
        except Exception as e:
            logger.error(f'Error parsing vacancies count: {e}')
            return
    finally:
        driver.quit()

