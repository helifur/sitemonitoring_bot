import asyncio
import aiofiles
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import json
import time
import difflib
import re

from lxml import etree


async def get_changes(link, class_name, chat_id):
    async with aiofiles.open("./assets/modules/parser/elements/elements.json") as file:
        all_elems = json.loads(await file.read())
        elems = all_elems[chat_id]

    # sitemap
    print(link[-3:])
    if link[-3:] == "xml":
        print("sitemap")
        driver = uc.Chrome()
        driver.maximize_window()

        driver.get(link)
        await asyncio.sleep(3)

        tree = etree.fromstring(driver.page_source)

        urls = [
            loc.text
            for loc in tree.findall(
                ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        ]

        lastmods = [
            lastmod.text
            for lastmod in tree.findall(
                ".//{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod"
            )
        ]

        sitemaps = {}

        for i in range(len(urls)):
            sitemaps[urls[i]] = lastmods[i]

        async with aiofiles.open(
            "./assets/modules/parser/elements/sitemaps.json"
        ) as file:
            all_data = json.loads(await file.read())
            data = all_data[chat_id]

        previous = data[link]

        ans = ""

        if not previous:
            data[link] = sitemaps
            all_data[chat_id] = data

            async with aiofiles.open(
                "./assets/modules/parser/elements/sitemaps.json", "w"
            ) as file:
                await file.write(json.dumps(all_data, indent=4))

            return None

        new_urls = set(urls) - set(previous.keys())
        removed_urls = set(previous.keys()) - set(urls)

        if new_urls or removed_urls:
            if new_urls:
                ans += "Добавлены URL:\n\n"
                for url in new_urls:
                    ans += url + "\n"
                ans += "\n=====================\n\n"

            if removed_urls:
                ans += "Удалены URL:\n"
                for url in removed_urls:
                    ans += url + "\n"
                ans += "\n=====================\n\n"
        else:
            return None

        flag = False

        for i in range(len(lastmods)):
            if lastmods[i] != previous.values()[i]:
                if not flag:
                    ans += "Изменения в lastmods:\n"
                    flag = True

                ans += f"URL: {urls[i]}\n"
                ans += f"Старый lastmod: {previous.values()[i]}\n"
                ans += f"Новый lastmod: {lastmods[i]}\n\n"

        data[link] = sitemaps
        all_data[chat_id] = data

        async with aiofiles.open(
            "./assets/modules/parser/elements/sitemaps.json", "w"
        ) as file:
            await file.write(json.dumps(all_data, indent=4))

        return ans

    "============================================="

    driver = uc.Chrome(use_subprocess=True)
    driver.maximize_window()

    driver.get(link)

    if "intickets" in re.search(r"(?:https://)?(?:www\.)?([^/]+)", link).group(1).split(
        "."
    ):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "scheme-canvas"))
            )

            await asyncio.sleep(2)

        except Exception:
            elems[link][class_name] = "Билеты распроданы!"
            all_elems[chat_id] = elems

            async with aiofiles.open(
                "./assets/modules/parser/elements/elements.json", "w"
            ) as file:
                await file.write(json.dumps(all_elems, indent=4))

            return None

    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        )

        await asyncio.sleep(2)

    except Exception:
        result = f"Элемент с классом {class_name} не был обнаружен!"

    print("Успешно загружено!")

    # name = re.search(r"(?:htts://)?(?:www\.)?([^/]+)", link).group(1)
    # print(name)

    content = elems[link][class_name]

    body_element = driver.find_element(By.CLASS_NAME, class_name)
    print("Элемент найден!")
    body_content = body_element.get_attribute("innerHTML")
    print("Содержимое: " + body_content[:10] + "...")

    driver.quit()
    # ua = UserAgent()
    # user_agent = ua.random

    # opts.add_argument(f"user-agent={user_agent}")
    # opts.add_argument("--disable-blink-features=AutomationControlled")
    # opts.add_argument("--disable-extensions")
    # opts.add_argument("--disable-gpu")

    # driver = uc.Chrome(options=opts)
    # driver = webdriver.Chrome(options=opts)

    # driver.maximize_window()

    # name = re.search(r"(?:https://)?(?:www\.)?([^/]+)", link).group(1)
    # print(name)

    if not content:
        elems[link][class_name] = body_content
        all_elems[chat_id] = elems

        async with aiofiles.open(
            "./assets/modules/parser/elements/elements.json", "w"
        ) as file:
            await file.write(json.dumps(all_elems, indent=4))

        return None

    result = difflib.ndiff(content.split("\n"), body_content.split("\n"))

    if result:
        changes = "\n".join(
            [line for line in result if line.startswith("-") or line.startswith("+")]
        )

        elems[link][class_name] = body_content
        all_elems[chat_id] = elems

        async with aiofiles.open(
            "./assets/modules/parser/elements/elements.json", "w"
        ) as file:
            await file.write(json.dumps(all_elems, indent=4))

        return changes

    else:
        return None

    # if body_content != content:

    # with open(data[name], "w") as f:
    # f.write(body_content)

    # with open("../../../data/data.json", "w") as file:
    # json.dump(data, file)
