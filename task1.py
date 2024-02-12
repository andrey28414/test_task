import pandas as pd
import aiohttp
import asyncio
from PIL import Image
import numpy as np
import io

async def fetch_image_size(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                image = Image.open(io.BytesIO(image_data))
                width, height = image.size
                return width, height
            else:
                return "nan"
    except Exception as e:
        return type(e).__name__

async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image_size(session, url) for url in urls]
        image_sizes = await asyncio.gather(*tasks)
    return image_sizes

async def entry(file_name, url_column, size_column, delimeter):
    excel_file = file_name
    df = pd.read_excel(excel_file, na_filter=False, dtype=str)
    urls = df[url_column].tolist()
    for i in range(3):
        empty_indexes = [index for index, item in enumerate(df[size_column]) if delimeter not in item]
        to_process = [urls[i] for i in empty_indexes]
        image_sizes = await process_urls(to_process)

        print(len(image_sizes))
        for index, j in enumerate(empty_indexes):
            item = image_sizes[index]
            if isinstance(item, tuple):
                df.loc[j, size_column] = f"{item[0]}"+delimeter+f"{item[1]}"
            else:
                df.loc[j, size_column] = item
        print("==================")
    df.to_excel(excel_file, index=False)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(entry(
        file_name="parser.xlsx",
        url_column='image_url',
        size_column='SIZE',
        delimeter='#'
    ))
