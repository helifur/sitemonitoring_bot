import asyncio
import aiofiles
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import json
import difflib
import re
import psutil

import assets.config.config

from lxml import etree


async def kill_driver_process(driver):
    try:
        # Найдем процесс по pid
        pid = driver.service.process.pid
        process = psutil.Process(pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
    except Exception as e:
        print(f"Ошибка при завершении процесса: {e}")


async def parse_intickets(driver, classname):
    try:
        # waiting for canvas appearing
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "scheme-canvas"))
        )

    except Exception:
        # waiting for canvas appearing
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "closed-sales"))
        )

    finally:
        # get element
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, classname))
        )

        body_content = element.get_attribute("innerHTML")
        driver.quit()
        return body_content


async def parse_timepad(driver):
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )

        driver.switch_to.frame(iframe)

        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "tpwf-loader-fadeable"))
        )
        await asyncio.sleep(2)

        body_content = element.get_attribute("innerHTML")
        driver.quit()
        return body_content

    except Exception:
        return None


async def parse_sitemap(driver, link, chat_id):
    print("sitemap " + str(chat_id))

    driver.get(link)
    tree = etree.fromstring(driver.page_source)
    driver.quit()

    urls = [
        loc.text
        for loc in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
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

    async with aiofiles.open("./assets/modules/parser/elements/sitemaps.json") as file:
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

        if removed_urls:
            ans += "\n\nУдалены URL:\n"
            for url in removed_urls:
                ans += url + "\n"

    else:
        flag = False

        for i in range(len(lastmods)):
            if lastmods[i] != list(previous.values())[i]:
                if not flag:
                    ans += "Изменения в lastmods:\n"
                    flag = True

                ans += f"URL: {urls[i]}\n"
                ans += f"Старый lastmod: {list(previous.values())[i]}\n"
                ans += f"Новый lastmod: {lastmods[i]}\n\n"

    data[link] = sitemaps
    all_data[chat_id] = data

    async with aiofiles.open(
        "./assets/modules/parser/elements/sitemaps.json", "w"
    ) as file:
        await file.write(json.dumps(all_data, indent=4))

    return ans


async def get_changes(link, class_name, chat_id):
    try:
        async with aiofiles.open(
            "./assets/modules/parser/elements/elements.json"
        ) as file:
            all_elems = json.loads(await file.read())
            elems = all_elems[chat_id]

        options = uc.ChromeOptions()

        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")

        assets.config.config.driver = uc.Chrome(options=options)

        assets.config.config.driver.maximize_window()

        if link[-3:] == "xml":
            return await parse_sitemap(assets.config.config.driver, link, chat_id)

        "============================================="

        assets.config.config.driver.get(link)

        if "timepad" in re.search(r"(?:https://)?(?:www\.)?([^/]+)", link).group(
            1
        ).split("."):
            body_content = await parse_timepad(assets.config.config.driver)

        elif "intickets" in re.search(r"(?:https://)?(?:www\.)?([^/]+)", link).group(
            1
        ).split("."):
            body_content = await parse_intickets(
                assets.config.config.driver, class_name
            )

        else:
            try:
                WebDriverWait(assets.config.config.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f".legend-top"))
                )
                await asyncio.sleep(2)

                body_element = assets.config.config.driver.find_element(
                    By.XPATH, f"//*[contains(@class, '{class_name}')]"
                )
                print("Элемент найден!")
                body_content = body_element.get_attribute("innerHTML")
                print("Содержимое: " + body_content[:10] + "...")

            except Exception:
                return f"Элемент с классом {class_name} не был обнаружен!"

        assets.config.config.driver.quit()
        await kill_driver_process(assets.config.config.driver)

        content = elems[link][class_name]

        if not content:
            elems[link][class_name] = body_content
            all_elems[chat_id] = elems

            async with aiofiles.open(
                "./assets/modules/parser/elements/elements.json", "w"
            ) as file:
                await file.write(json.dumps(all_elems, indent=4))

            return None

        if not body_content:
            assets.config.config.driver.quit()
            await kill_driver_process(assets.config.config.driver)
            return f"Элемент с классом {class_name} не найден!"

        result = difflib.ndiff(content.split("\n"), body_content.split("\n"))

        if result:
            changes = "\n".join(
                [
                    line
                    for line in result
                    if line.startswith("-") or line.startswith("+")
                ]
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

    except asyncio.CancelledError:
        print("CancelledError")
        assets.config.config.driver.quit()
        await kill_driver_process(assets.config.config.driver)
        raise
