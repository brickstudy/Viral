from src.oliveyoung.brand import Brand
from src.oliveyoung.items import Items
from src.utils.utils import write_local_as_json, current_datetime_getter
from src.utils.logger import Logging
from src.utils.utils import get_brand_url

import time
import random


logger = Logging("oliveyoung_scrapper").get_logger()


def oliveyoung_brand_scrapping():
    brand = Brand()
    brand.crawl_brand_metadata()
    write_local_as_json(brand.brand_metadata, './logs', f"brand_{str(current_datetime_getter())}")


def oliveyoung_items_reviews_crawling(driver, brand_name, brand_url):
    """
    :brand_name: 브랜드 이름 eg. "컬러그램", "페리페라"
    :brand_code: 올리브영 상에 매핑되어있는 브랜드 코드 eg. "A002712", "A000511"
    """
    logger.info(
        "start to get item scrapping of %s",
        brand_name
    )
    item_x = Items(brand_name, brand_url, logger, driver)
    item_x.crawl_total_items()
    logger.info(
        "getting %s's items is done\n%s",
        brand_name,
        item_x.data.keys()
    )

    item_list = item_x.data.keys()
    for item in item_list:
        try:
            item_x.crawl_reviews_in_each_items(item_id=item)
        except Exception:
            logger.error(
                "fail during getting %s",
                item
            )
            time.sleep(random.randrange(5, 7) + random.random())
            continue

    logger.info(
        "write %s as file",
        brand_name
    )
    write_local_as_json(item_x.data, './logs', f"{brand_name}_items")


# TODO
def main_brand(driver, **kwargs):
    pass


def main_item(driver, **kwargs):
    # 최초 entrypoint arg로 받은 수집 대상 브랜드 리스트
    brand = kwargs.get("brand")
    brand_url = get_brand_url(brand)
    oliveyoung_items_reviews_crawling(driver, brand, brand_url)


if __name__ == '__main__':
    # oliveyoung_brand_scrapping()
    oliveyoung_items_reviews_crawling()