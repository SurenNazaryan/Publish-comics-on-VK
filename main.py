import requests
import os
from dotenv import load_dotenv
from telegram import Bot
import random


def get_random_comic_number():
    last_comic_json_url = 'https://xkcd.com/info.0.json'
    response = requests.get(last_comic_json_url)
    response.raise_for_status()
    response = response.json()
    last_comic_number = response['num']
    random_number = random.randint(1, last_comic_number)
    return random_number


def fetch_comic_comment_filename(random_number):
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    file_url = response['img']
    comment = response['alt']

    response = requests.get(file_url)
    response.raise_for_status()
    file_name = os.path.basename(file_url)
    with open(file_name, 'wb') as file:
        file.write(response.content)
    return comment, file_name


def publish_comic(
    telegram_channel_id,
    telegram_bot_token,
    image_to_send,
    comment
):
    bot = Bot(token=telegram_bot_token)
    with open(image_to_send, 'rb') as file:
        bot.send_photo(
            chat_id=telegram_channel_id,
            photo=file,
            caption=comment
        )


if __name__ == '__main__':
    load_dotenv()
    telegram_channel_id = os.environ['TELEGRAM_CHANNEL_ID']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    random_number = get_random_comic_number()
    comment, file_name = fetch_comic_comment_filename(random_number)
    try:
        publish_comic(telegram_channel_id, telegram_bot_token, file_name, comment)
    except Exception:
        print('Картинка в ТГ не отправилась')
    finally:
        os.remove(file_name)

