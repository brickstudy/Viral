from selenium import webdriver
from tempfile import mkdtemp

from src.utils.logger import Logging
from src.oliveyoung.main import main_brand
from src.oliveyoung.main import main_item
# from src.youtube.main import main


logger = Logging("Handler").get_logger()


def handler(event=None, context=None):

    def driver_getter(user_agent="Mozilla/5.0"):
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

    # handler 함수 event argument 파싱 - user_agent
    user_agent = event.get("user_agent", "")

    # selenium webdriver 생성
    driver = driver_getter(user_agent=user_agent)
    try:
        assert driver
    except Exception as e:
        logger.error(
            "driver is not created successfully. Here's the exception %s",
            e
        )
        
    # handler 함수 event argument 파싱 - platform, details
    platform = event.get("platform", "").lower()
    if platform not in ["youtube", "oliveyoung"]:
        logger.error(
            "Invalid platform. Supported: 'youtube', 'oliveyoung'"
        )
        return {"error": "Invalid platform. Supported: 'youtube', 'oliveyoung'"}

    details = event.get("details", {})

    # 올리브영 또는 유튜브 수집기 동작
    if platform == 'oliveyoung':
        if details.get("target") == "brand":
            main_brand(driver, **details)
        else:
            main_item(driver, **details)
    # else:
    #     main(driver, **details)

    return
