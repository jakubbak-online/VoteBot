# selenium imports
import chromedriver_autoinstaller_fix
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

# std library
from time import sleep
import random
import logging
from datetime import datetime

# timing decorator
from mierz_czas import mierz_czas


# logging setup
log_path = f"logs/{datetime.now().date()}_{datetime.now().timestamp()}.log"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_path,
                    filemode='x')

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)


IGNORED_EXCEPTIONS = (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

chromedriver_autoinstaller_fix.install()


@mierz_czas
def vote():
    # define options
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")

    # headless flags as a bot
    # chrome_options.add_argument("--headless")

    # instantiate driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.minimize_window()

    site_link = "https://www.granice.pl/biblioteki"

    useragentarray = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    ]

    driver.get(site_link)
    driver.implicitly_wait(3)

    wait = WebDriverWait(driver, 30)

    consent_element = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'fc-button-label')))
    consent_element.click()

    driver.implicitly_wait(15)

    search_city = wait.until(expected_conditions.element_to_be_clickable((By.ID, "search_city")))
    search_city.click()

    search_city.send_keys("Jastrzębie-Zdrój")

    first_element = driver.find_element(By.CLASS_NAME, "ui-menu-item-wrapper")
    first_element.click()

    vote_button = driver.find_element(By.CLASS_NAME, "buttonV")
    vote_button.click()

    try:
        message = driver.find_element(By.CLASS_NAME, "success-message").text
    except NoSuchElementException:
        message = driver.find_element(By.CLASS_NAME, "error-message").text
    print(message)

    sleep(5)
    return message

    # driver.close()


iteration = 0
while True:
    iteration += 1
    print(f"-------------------- Iteracja {iteration} --------------------")
    returned_message = vote()
    print(returned_message)
    print(f"--------------------------------------------------------------")

    seconds_to_wait = round(random.uniform(135, 165), 2)
    print(f"Gonna wait {seconds_to_wait} seconds\n\n")
    sleep(seconds_to_wait)
