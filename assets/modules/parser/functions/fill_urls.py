import json
import aiofiles


async def fill_urls(chat_id):
    """
    This function fills in the json that the parser uses when /tracking is invoked
    """
    async with aiofiles.open("./assets/data/data.json") as f:
        data = json.loads(await f.read())

    try:
        data = data[str(chat_id)]

    except KeyError:
        return True

    result = {str(chat_id): {}}

    for key, value in data.items():
        result[str(chat_id)][key] = {i: "" for i in value}

    async with aiofiles.open(
        "./assets/modules/parser/elements/elements.json", "w"
    ) as f:
        await f.write(json.dumps(result, indent=4))

    result[str(chat_id)] = {i: "" for i in data.keys() if i[-3:] == "xml"}

    async with aiofiles.open(
        "./assets/modules/parser/elements/sitemaps.json", "w"
    ) as f:
        await f.write(json.dumps(result, indent=4))

    return True
