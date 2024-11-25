from src.oliveyoung.brand import Brand
from src.oliveyoung.items import Items
from src.utils import write_local_as_json


def oliveyoung_brand_scrapping():
    brand = Brand()
    brand.crawl_brand_metadata()
    print(brand.brand_metadata)


def oliveyoung_items_reviews_crawling():
    brand_name_lst = ["에스트라"]
    brand_url_lst = ["https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd=A002474"]

    for brand_name, brand_url in zip(brand_name_lst, brand_url_lst):
        print(f"start {brand_name}")
        item_x = Items(brand_name, brand_url)
        item_x.crawl_total_items()
        print(f"getting {brand_name}'s items is done")
        print(item_x.data)

        item_list = item_x.data.keys()
        for item in item_list:
            try:
                item_x.crawl_reviews_in_each_items(item_id=item)
            except Exception:
                print("fail during getting {}")
                write_local_as_json(item_x.data, './logs', f"{brand_name}_items")


if __name__ == '__main__':
    # 브랜드 정보 수집
    oliveyoung_brand_scrapping()
    # 아이템 정보, 해당 아이템의 리뷰 수집
    oliveyoung_items_reviews_crawling()
