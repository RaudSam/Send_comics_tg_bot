import requests
import telegram
import asyncio
import os
from dotenv import load_dotenv
from random import randint
        

def get_comic_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_numb = response.json()['num']
    return comic_numb


def get_comics(comic_numb):
    random_numb = randint(1, comic_numb)
    url = f'https://xkcd.com/{random_numb}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json() 
    comments = comic['alt']
    image_path = comic['img']
    image_respone = requests.get(image_path)
    image_respone.raise_for_status()
    image_name = f'image_{random_numb}.png' 
    with open(image_name, 'wb') as file:
        file.write(image_respone.content)
    return image_name, comments


async def publish_a_comics(image_name, comments, token, chat_id):
    bot = telegram.Bot(token = token)
    bot.send_message(chat_id=chat_id, text=comments)
    with open(image_name, 'rb') as file:
        await bot.send_photo(chat_id=chat_id, photo=file)


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')

    comic_numb = get_comic_number()
    try:
        image_name, comments = get_comics(comic_numb)
        asyncio.run(publish_a_comics(image_name, comments, token, chat_id))
    finally:
        if os.path.exists(image_name):
            os.remove(image_name)