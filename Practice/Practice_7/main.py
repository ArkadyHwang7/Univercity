import re
import csv
import urllib.request
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "Practic7.csv")

url = "https://msk.spravker.ru/avtoservisy-avtotehcentry/"
html = urllib.request.urlopen(url).read().decode("utf-8")

block_pattern = r'(?s)<div class="widgets-list__item">(.*?)(?=<div class="widgets-list__item">|$)'

name_pattern  = r'class="org-widget-header__title-link">(.*?)</a>'
addr_pattern  = r'meta--location">\s*(.*?)\s*</span>'
phone_pattern = r'Телефон</span>.*?class="spec__value">(.*?)</dd>'
time_pattern  = r'Часы работы</span>.*?class="spec__value">(.*?)</dd>'

blocks = re.findall(block_pattern, html)

with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Название", "Адрес", "Телефон", "Время работы"])

    for b in blocks:
        name  = re.search(name_pattern, b, re.S)
        addr  = re.search(addr_pattern, b, re.S)
        phone = re.search(phone_pattern, b, re.S)
        time  = re.search(time_pattern, b, re.S)

        if not name:
            continue

        writer.writerow([
            name.group(1).strip(),
            addr.group(1).strip() if addr else "",
            phone.group(1).strip() if phone else "",
            time.group(1).strip() if time else ""
        ])
