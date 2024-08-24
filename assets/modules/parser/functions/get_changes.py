import asyncio
import aiofiles
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import difflib

from lxml import etree


async def get_changes(link, class_name):
    async with aiofiles.open("./assets/modules/parser/elements/elements.json") as file:
        elems = json.loads(await file.read())

    # sitemap
    print(link[-3:])
    if link[-3:] == "xml":
        print("sitemap")
        driver = Chrome()
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

        async with aiofiles.open(
            "./assets/modules/parser/elements/sitemaps.json"
        ) as file:
            data = json.loads(await file.read())

        previous = data[link]

        new_urls = set(urls) - set(previous)
        removed_urls = set(previous) - set(urls)

        ans = ""

        if not previous:
            data[link] = urls

            async with aiofiles.open(
                "./assets/modules/parser/elements/sitemaps.json", "w"
            ) as file:
                await file.write(json.dumps(data, indent=4))

            return None

        if new_urls or removed_urls:
            if new_urls:
                ans += "Добавлены URL:\n\n"
                for url in new_urls:
                    ans += url + "\n"
            if removed_urls:
                ans += "Удалены URL:\n"
                for url in removed_urls:
                    ans += url + "\n"
        else:
            return None

        data[link] = urls

        async with aiofiles.open(
            "./assets/modules/parser/elements/sitemaps.json", "w"
        ) as file:
            await file.write(json.dumps(data, indent=4))

        return ans

    driver = Chrome()
    driver.maximize_window()

    driver.get(link)
    WebDriverWait(driver, 7).until(
        EC.visibility_of_element_located((By.CLASS_NAME, class_name))
    )
    await asyncio.sleep(3)

    print("Успешно загружено!")

    # name = re.search(r"(?:htts://)?(?:www\.)?([^/]+)", link).group(1)
    # print(name)

    content = elems[link][class_name]

    body_element = driver.find_element(By.CLASS_NAME, class_name)
    print("Элемент найден!")
    body_content = body_element.get_attribute("innerHTML")
    print("Содержимое: " + body_content[:10] + "...")

    if not content:
        elems[link][class_name] = body_content

        async with aiofiles.open(
            "./assets/modules/parser/elements/elements.json", "w"
        ) as file:
            await file.write(json.dumps(elems, indent=4))

        return None

    result = difflib.ndiff(content.split("\n"), body_content.split("\n"))

    if result:
        changes = "\n".join(
            [line for line in result if line.startswith("-") or line.startswith("+")]
        )

        elems[link][class_name] = body_content

        async with aiofiles.open(
            "./assets/modules/parser/elements/elements.json", "w"
        ) as file:
            await file.write(json.dumps(elems, indent=4))

        return changes

    else:
        return None

    # if body_content != content:

    # with open(data[name], "w") as f:
    # f.write(body_content)

    # with open("../../../data/data.json", "w") as file:
    # json.dump(data, file)
