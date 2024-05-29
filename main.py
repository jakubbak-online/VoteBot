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
import re

from user_agents import user_agents

# timing decorator
from mierz_czas import mierz_czas
from config import to_sleep_if_error, site_link, city_name

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

# --- CONSTANTS ---
IGNORED_EXCEPTIONS = (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)


def sleep_between_actions():
    sleep(round(random.uniform(0.5, 1.5), 2))


chromedriver_autoinstaller_fix.install()


@mierz_czas
def vote() -> str:
    # define options
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")

    # disable the AutomationControlled feature of Blink rendering engine
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # headless flags as a bot
    # chrome_options.add_argument("--headless")

    user_agent_to_use = random.choice(user_agents)
    chrome_options.add_argument(f"--user-agent={user_agent_to_use}")

    # instantiate driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.minimize_window()

    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent_to_use})

    # Check user agent
    print(driver.execute_script("return navigator.userAgent"))

    driver.get(site_link)
    driver.implicitly_wait(3)

    sleep_between_actions()

    wait = WebDriverWait(driver, 30)

    consent_element = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'fc-button-label')))
    consent_element.click()

    # driver.implicitly_wait(15)
    sleep_between_actions()

    search_city = wait.until(expected_conditions.element_to_be_clickable((By.ID, "search_city")))

    sleep_between_actions()
    driver.execute_script(f'window.scrollTo(0, {random.randint(500, 756)})')

    sleep_between_actions()
    search_city.click()

    search_city.send_keys(city_name)
    sleep_between_actions()

    first_element = driver.find_element(By.CLASS_NAME, "ui-menu-item-wrapper")
    sleep_between_actions()
    first_element.click()

    vote_button = driver.find_element(By.CLASS_NAME, "buttonV")
    sleep_between_actions()
    vote_button.click()

    # Detect message
    try:
        message = driver.find_element(By.CLASS_NAME, "success-message").text
    except NoSuchElementException:
        message = driver.find_element(By.CLASS_NAME, "error-message").text

    if bool(re.search(r"bot", message)) is True:
        print(f"Sleeping {to_sleep_if_error} seconds")
        sleep(to_sleep_if_error)

    print(message)
    return message

    # driver.close()


iteration = 0
while True:
    iteration += 1
    message_to_send = f"{datetime.now()} ----------- Iteracja {iteration} -----------"

    logging.log(logging.DEBUG, message_to_send)
    print(message_to_send)
    vote()
    print(f"--------------------------------------------------------------")

    seconds_to_wait = round(random.uniform(160, 190), 2)
    print(f"Gonna wait {seconds_to_wait} seconds\n\n")
    sleep(seconds_to_wait)
