import json
import requests
from time import sleep
from threading import Thread


# store to db in future ...
feed_py = []
feed_js = []
feed_trend = []


def get_config():
    with open("config/config.json", "r") as read_file:
        return json.load(read_file)


class Telegram:
    def __init__(self, chat_id):
        self.token = get_config()["telegram_token"]
        self.chat_id = chat_id

    def send_message(self, msg):
        while True:
            sleep(1)
            res = requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage?text={msg}&chat_id={self.chat_id}")
            if res.ok:
                break


class Feed:
    def __init__(self, lang, period):
        self.lang = lang
        self.period = period

    def get_feed(self):
        url = f'https://ghapi.huchen.dev/repositories?language={self.lang}&since={self.period}'
        while True:
            sleep(1)
            res = requests.get(url)
            if res.ok:
                return [v for msg in res.json() for k, v in msg.items() if k == 'url']


def feed(chat_id, lang, period):
    global feed_py
    global feed_js
    global feed_trend

    try:
        if lang == 'python':
            start_feed = feed_py
        elif lang == 'javascript':
            start_feed = feed_js
        elif lang == 'jupyter-notebook':
            start_feed = feed_trend

        feed_instance = Feed(lang, period)
        tg = Telegram(chat_id)

        while True:
            new_feed = feed_instance.get_feed()

            if len(start_feed) == 0:
                start_feed = new_feed

                if len(start_feed) > 30:
                    del(start_feed[:5])

            for item in new_feed:
                if item not in start_feed:
                    start_feed.append(item)
                    tg.send_message(item)
                    sleep(5)
            sleep(3600)
    except Exception as e:
        tg.send_message(e)


def main():
    channels = [v for k, v in get_config().items() if 'channel' in k]

    t1 = Thread(target=feed, args=(
        channels[0][0], channels[0][1], channels[0][2]),)
    t2 = Thread(target=feed, args=(
        channels[1][0], channels[1][1], channels[1][2]),)
    t3 = Thread(target=feed, args=(
        channels[2][0], channels[2][1], channels[2][2]),)

    t1.start()
    t2.start()
    t3.start()



if __name__ == "__main__":
    main()
