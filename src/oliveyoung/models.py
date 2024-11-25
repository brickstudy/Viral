from dataclasses import dataclass, field
from typing import List


@dataclass
class OliveyoungBrand:
    query_keyword: List[str]            # api 쿼리 키워드 - 브랜드 영문이름 등
    brand_shop_detail_url: str          # 브랜드관 url
    category: List[str]                 # 브랜드가 속한 카테고리
    released_date: str = field(default_factory='2024/08/05')   # 신제품 출시 일자


def brand_generator():
    return OliveyoungBrand(
        [],
        '',
        [],
        ''
    )


@dataclass
class OliveyoungItem:
    item_name: str
    item_detail_url: str
    is_in_promotion: bool
    reviews: List[str]


def oliveyoung_item_generator():
    return OliveyoungItem(
        '',
        '',
        False,
        []
    )