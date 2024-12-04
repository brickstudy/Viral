from src.oliveyoung.brand import Brand
from src.oliveyoung.items import Items
from src.utils.utils import write_local_as_json, current_datetime_getter
from src.utils.logger import Logging

import time
import random


logger = Logging("oliveyoung_scrapper").get_logger()


def oliveyoung_brand_scrapping():
    brand = Brand()
    brand.crawl_brand_metadata()
    write_local_as_json(brand.brand_metadata, './logs', f"brand_{str(current_datetime_getter())}")


def oliveyoung_items_reviews_crawling():
    brand_name_lst = ["롬엔", "컬러그램", "페리페라", "토니모리", "바닐라코"]
    brand_code_lst = ["A001833", "A002712", "A000511", "A003693", "A002759"]

    for brand_name, brand_code in zip(brand_name_lst, brand_code_lst):
        logger.info(
            "start to get item scrapping of %s",
            brand_name
        )
        brand_url = f"https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd={brand_code}"

        item_x = Items(brand_name, brand_url)
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


if __name__ == '__main__':
    # 브랜드 정보 수집
    # oliveyoung_brand_scrapping()
    # 아이템 정보, 해당 아이템의 리뷰 수집
    oliveyoung_items_reviews_crawling()
