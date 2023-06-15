# -*- coding: windows-1251 -*-
import json
import requests
import re
from fake_headers import Headers
from bs4 import BeautifulSoup

if __name__ == "__main__":

    HOST = "https://spb.hh.ru"
    PARAMS = {
        "area": ["1", "2"],
        "currency_code": "USD",
        "search_field": ["name", "company_name", "description"],
        "enable_snippets": "true",
        "text": "Python",
        "no_magic": "true",
        "ored_clusters": "true",
        }

    url = f"{HOST}/search/vacancy"
    HEADERS = Headers(browser="firefox", os="win").generate()
    response = requests.get(url, params=PARAMS, headers=HEADERS)
    text = response.text
    soup = BeautifulSoup(text, features='html.parser')
    items = soup.find_all("div", class_="vacancy-serp-item__layout")
    result = []

    for item in items:
        title = item.find(class_="serp-item__title").text
        desc = soup.find(class_='g-user-content').text

        if "django" in desc.lower() or "flask" in desc.lower():
            link = item.find("a", class_="serp-item__title").get("href")
            salary = item.find("span", class_="bloko-header-section-3")

            if salary is not None:
                salary = salary.text
            else:
                salary = "Зарплата не указана!"

            company_name = item.find("div", class_="vacancy-serp-item__meta-info-company").text
            city = item.find("div", attrs={"data-qa": "vacancy-serp__vacancy-address"}).text

            result.append({
                "Вакансия": title,
                "Вилка зп": re.sub(r"(\u202f)", " ", salary),
                "Название компании": re.sub(r"(\xa0)", " ", company_name),
                "Город": re.sub(r"(\xa01\xa0)", " ", city),
                "Ссылка": link
            })

    with open("result.json", "w", encoding="utf8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
