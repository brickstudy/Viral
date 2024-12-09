from selenium import webdriver
from tempfile import mkdtemp

from utils.logger import Logging


logger = Logging("Handler").get_logger()


def handler(event=None, context=None, chrome=None, user_agent=None):

    def driver_getter(chrome=None, user_agent="Mozilla/5.0"):
        if chrome is None:
            options = webdriver.ChromeOptions()
            service = webdriver.ChromeService("/opt/chromedriver")

            options.binary_location = '/opt/chrome/chrome'
            options.add_argument("--headless=new")
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280x1696")
            options.add_argument("--single-process")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-dev-tools")
            options.add_argument("--no-zygote")
            options.add_argument(f"--user-data-dir={mkdtemp()}")
            options.add_argument(f"--data-path={mkdtemp()}")
            options.add_argument(f"--disk-cache-dir={mkdtemp()}")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument(f"--user-agent={user_agent}")

            return webdriver.Chrome(options=options, service=service)
        return chrome

    chrome = driver_getter(user_agent=user_agent)
    try:
        assert chrome
    except Exception as e:
        logger.error(
            "chrome is not created successfully. Here's the exception %s",
            e
        )

    return
