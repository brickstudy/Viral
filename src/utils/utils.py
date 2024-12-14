import urllib
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup

from dataclasses import asdict

import random
import time
import json
import os
from datetime import datetime


def get_soup(url: str = None) -> BeautifulSoup:
    user_agent_lst = ['Googlebot', 'Yeti', 'Daumoa', 'Twitterbot']
    user_agent = user_agent_lst[random.randint(0, len(user_agent_lst) - 1)]
    headers = {'User-Agent': user_agent}

    try:
        req = urllib.request.Request(url, headers=headers)
        page = urlopen(req)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
    except (HTTPError, URLError) as e:
        print(f"HTTP/URL error {e}")
        time.sleep(5)
    except (ValueError) as e:
        print(f"Value error {e}")
        soup = None
    else:
        return soup


def write_local_as_json(data: dict, file_path: str, file_name: str) -> None:
    """
    data : dictionary with the dataclass value
    file_path : directory string where the json file created
    file_name : file name without extension
    """
    try:
        os.makedirs(file_path, exist_ok=True)
    except PermissionError:
        print("*** write_local_as_json cannot create given directory ***")
        raise

    path = f"{file_path}/{file_name}.json"
    json_data = {b_name: asdict(details) for b_name, details in data.items()}
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)


def read_local_as_dict(file_path: str, file_name: str) -> dict:
    from src.oliveyoung.models import OliveyoungBrand

    path = f"{file_path}/{file_name}.json"
    with open(path, 'r', encoding='utf-8') as json_file:
        loaded_data = json.load(json_file)

    for key, val in loaded_data.items():
        loaded_data[key] = OliveyoungBrand(**val)
    return loaded_data


def current_datetime_getter():  
    current_time = datetime.now()
    current_datetime = current_time.strftime("%Y%m%d_%H%M%S")
    return current_datetime


def get_workdir():
    """
    실행시스템경로/Viral 경로 리턴
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_total_brand_lst() -> list:
    brand_data_json_path = os.path.join(get_workdir(), 'config.json')
    with open(brand_data_json_path, 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
    return loaded_data['keywords']


def get_user_agent_lst() -> str:
    brand_data_json_path = os.path.join(get_workdir(), 'config.json')
    with open(brand_data_json_path, 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
    return loaded_data['headers']['user-agent']
