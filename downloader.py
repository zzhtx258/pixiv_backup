import asyncio
import aiohttp
import os
import logging
from login import login
from get_favourites import get_favorites

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROXY = "socks5://127.0.0.1:7897"  # replace with your own proxy
OUTPUT_DIR = "./public"
OUTPUT_DIR1 = "./private"

async def download_image(session, url, filename):
    headers = {"Referer": "https://www.pixiv.net/"}
    try:
        async with session.get(url, headers=headers, proxy=PROXY) as response:
            if response.status == 200:
                content = await response.read()
                if content:
                    with open(filename, 'wb') as f:
                        f.write(content)
                    logger.info(f"image saved to:{filename}")
                else:
                    logger.warning(f"empty image:{url}")
            else:
                logger.error(f"Failed download, status code:{response.status},URL:{url}")
    except Exception as e:
        logger.error(f"Failed to download:{e}")

async def download_all_images(api, illust_ids, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for illust_id in illust_ids:
            detail = api.illust_detail(illust_id)
            if (not detail.illust):
                print("unavaliable work!")
                continue
            if (detail.illust.meta_pages):
                cnt = 0
                for page in detail.illust.meta_pages:
                    image_url = page.image_urls['large']
                    filename = os.path.join(output_dir, f"{illust_id}_{cnt}.jpg")
                    logger.info(f"ready to download image:{image_url}")
                    tasks.append(download_image(session, image_url, filename))
                    cnt+=1
            else:
                image_url = detail.illust.image_urls['large']
                filename = os.path.join(output_dir, f"{illust_id}.jpg")
                logger.info(f"ready to download image:{image_url}")
                tasks.append(download_image(session, image_url, filename))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    api = login()

    illust_ids = get_favorites(api, "public")
    illust_ids1 = get_favorites(api, "private")

    asyncio.run(download_all_images(api, illust_ids, OUTPUT_DIR))
    asyncio.run(download_all_images(api, illust_ids1, OUTPUT_DIR1))