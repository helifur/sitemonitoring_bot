from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
import difflib


async def manage_page(link, class_name):
    with open("./assets/modules/parser/elements/elements.json") as file:
        elems = json.load(file)

    driver = Chrome()
    driver.maximize_window()

    driver.get(link)
    WebDriverWait(driver, 7).until(
        EC.visibility_of_element_located((By.CLASS_NAME, class_name))
    )
    time.sleep(3)

    print("Успешно загружено!")

    # name = re.search(r"(?:https?://)?(?:www\.)?([^/]+)", link).group(1)
    # print(name)

    content = elems[link][class_name]

    body_element = driver.find_element(By.CLASS_NAME, class_name)
    print("Элемент найден!")
    body_content = body_element.get_attribute("innerHTML")
    print("Содержимое: " + body_content[:10] + "...")

    result = difflib.ndiff(content.split("\n"), body_content.split("\n"))

    if result:
        changes = "\n".join(
            [line for line in result if line.startswith("-") or line.startswith("+")]
        )

        # Отправляем результат пользователю
        with open("./assets/modules/parser/elements/elements.json", "w") as file:
            elems[link][class_name] = body_content

            json.dump(elems, file)

        return f"Изменения между строками:\n{changes}"

    else:
        return "Изменений нет."

    # if body_content != content:

    # with open(data[name], "w") as f:
    # f.write(body_content)

    # with open("../../../data/data.json", "w") as file:
    # json.dump(data, file)
