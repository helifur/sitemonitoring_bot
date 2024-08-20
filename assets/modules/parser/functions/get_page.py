from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
import json
import difflib

if __name__ == "__main__":
    link = "https://iframeab-pre4791.intickets.ru/"
    class_name = "home"

    with open("../../../data/data.json") as file:
        data = json.load(file)

    driver = Chrome()
    driver.maximize_window()

    driver.get(link)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, class_name))
    )
    time.sleep(3)

    print("Успешно загружено!")

    name = re.search(r"(?:https?://)?(?:www\.)?([^/]+)", link).group(1)
    print(name)

    if name not in data.keys():
        data[name] = f"../../../data/pages/{data["site_counter"]}.html"

        with open(data[name], "w") as f:
            body_element = driver.find_element(By.CLASS_NAME, class_name)
            body_content = body_element.get_attribute("innerHTML").replace("\n", "")

            f.write(body_content)

        data["site_counter"] += 1

    else:
        with open(data[name], "r", encoding="utf-8") as f:
            content = f.read()

            body_element = driver.find_element(By.CLASS_NAME, class_name)
            print("Элемент найден!")
            body_content = body_element.get_attribute("innerHTML").replace("\n", "")
            print("Содержимое: " + body_content[:10] + "...")

            if body_content != content:
                print("ALERT!")

                d = difflib.HtmlDiff()

                # Получение HTML-таблицы с различиями
                html_diff = d.make_file(body_content.splitlines(), content.splitlines())

                # Сохранение в файл
                with open("diff.html", "w") as f:
                    f.write(html_diff)

                with open(data[name], "w") as f:
                    f.write(body_content)

    with open("../../../data/data.json", "w") as file:
        json.dump(data, file)
