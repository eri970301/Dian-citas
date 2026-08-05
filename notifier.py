import requests

from config import BOT_TOKEN
from config import CHAT_ID


class TelegramNotifier:

    def __init__(self):

        self.url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    def send(self, message):

        try:

            r = requests.post(

                self.url,

                json={

                    "chat_id": CHAT_ID,

                    "text": message

                },

                timeout=20

            )

            r.raise_for_status()

            return True

        except Exception as ex:

            print(ex)

            return False