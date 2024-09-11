import json
import aiofiles


async def fill_urls():
    """
    This function fills in the json that the parser uses when /tracking is invoked
    """
    async with aiofiles.open("./assets/data/data.json") as f:
        data = json.loads(await f.read())

    # try:
    #     data = data[str(chat_id)]

    # except KeyError:
    #     return True

    result = {}

    for chat_id in data.keys():
        result[chat_id] = {}
        for link, classes in data[chat_id].items():
            result[chat_id][link] = {i: "" for i in classes}

    async with aiofiles.open(
        "./assets/modules/parser/elements/elements.json", "w"
    ) as f:
        await f.write(json.dumps(result, indent=4))

    result = {}

    for chat_id in data.keys():
        result[chat_id] = {}
        for link in data[chat_id].keys():
            if link[-3:] == "xml":
                result[str(chat_id)][link] = ""
    # result[str(chat_id)] = {i: "" for i in data.keys() if i[-3:] == "xml"}

    async with aiofiles.open(
        "./assets/modules/parser/elements/sitemaps.json", "w"
    ) as f:
        await f.write(json.dumps(result, indent=4))

    return True
