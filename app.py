import json
import requests
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


last_run_date = datetime.utcnow() - timedelta(days=1)


def get_config():
    with open("config/config.json", "r") as read_file:
        return json.load(read_file)


def telegram_send_message(telegram_token, chat_id, msg):
    while True:
        res = requests.get(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage?text={msg}&chat_id={chat_id}&parse_mode=MARKDOWN")
        if res.json().get('ok'):
            break
        sleep(5)


def get_res(url):
    while True:
        headers = {'User-Agent':'Chrome/85.0.4183.121'}
        res = requests.get(url, headers=headers)
        if res.ok:
            return res
        sleep(5)


def get_feed(url):
    formated_articles = []
    res = get_res(url).text
    soup = BeautifulSoup(res, 'html.parser')
    articles = soup.find_all("article", {"class": "Box-row"})
    for article in articles:
        try:
            title = article.h1.text.replace(
                ' ', '').replace('\n', '').split('/')[1]
        except Exception:
            title = "Something wrong (title) ..."
        try:
            description = article.p.text.replace(
                '\n', '').lstrip().rstrip()
        except Exception:
            description = 'No description'
        try:
            stars = article('a', {'class': "muted-link d-inline-block mr-3"}
                            )[0].text.replace(' ', '').replace('\n', '')
        except Exception:
            stars = "Something wrong (stars) ..."
        try:
            stars_total = f'{stars} stars total'
            stars_today = article('span', {'class': 'd-inline-block float-sm-right'})[
                0].text.replace('\n', '').lstrip().rstrip()
        except Exception:
            stars_total = "Something wrong (stars_total) ..."
        try:
            link = article.h1.a.text.replace(' ', '').replace('\n', '')
            final_link = f"https://github.com/{link}"
        except Exception:
            stars_total = "Something wrong (link) ..."
        formated_articles.append(
            f'*{title}*\n\n{description}\n\n*{stars_total}*\n\n*{stars_today}*\n\n[View on Github.com]({final_link})')
    return formated_articles


def main():
    global last_run_date
    try:
        config = get_config()
        telegram_token = config['telegram_token']
        chat_id = config['chat_id']
        coding_lang = config['coding_lang']
        url = f'https://github.com/trending/{coding_lang}?since=daily&spoken_language_code=en'
        if datetime.utcnow() > last_run_date + timedelta(days=1):
            msgs = get_feed(url)
            for msg in msgs:
                if '&' in msg:
                    msg = msg.replace('&', '')
                telegram_send_message(telegram_token, chat_id, msg)
                sleep(5)
            last_run_date = datetime.utcnow()
    except Exception as e:
        telegram_send_message(telegram_token, chat_id, str(e))


if __name__ == "__main__":
    while True:
        main()
