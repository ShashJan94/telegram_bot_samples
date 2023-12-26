import os
import json
from telebot import TeleBot
import time
class TelegramMessenger:
    def __init__(self, bot_token, chat_id, data_dir):
        self.bot = TeleBot(token=bot_token)
        self.chat_id = chat_id
        self.data_dir = data_dir

    def send_message(self, title, url, timestamp):
        message = f"Title: {title}\nURL: {url}\nTimestamp: {timestamp}"
        self.bot.send_message(chat_id=self.chat_id, text=message)

    def send_messages_from_sorted_json_files(self):
        # List all JSON files in the data directory
        json_files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]

        # Sort the JSON files by creation time (oldest first)
        json_files.sort(key=lambda x: os.path.getctime(os.path.join(self.data_dir, x)))

        for json_filename in json_files:
            try:
                time.sleep(100)
                with open(os.path.join(self.data_dir, json_filename), 'r') as json_file:
                    data = json.load(json_file)

                    # Extract information from the JSON data
                    title = data.get('title', 'No title available')
                    url = data.get('url', '')
                    timestamp = data.get('timestamp', 'No timestamp available')

                    # Send the message to Telegram using the send_message method
                    self.send_message(title, url, timestamp)
            except FileNotFoundError:
                print(f"JSON file '{json_filename}' not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

# Usage example:
if __name__ == '__main__':
    # Replace with your actual bot token, chat ID, and data directory
    BOT_TOKEN = '6520699737:AAHqnUlHw7VdGYuglehCll7pXC8VqBN1Q4Y'
    CHANNEL_NAME = '@thehindutribune'
    DATA_DIR = os.path.join(os.curdir+'data_files')
    print(DATA_DIR)

    # Create an instance of the TelegramMessenger class
    telegram_messenger = TelegramMessenger(BOT_TOKEN, CHANNEL_NAME, DATA_DIR)

    # Send messages from all sorted JSON files in the data directory
    telegram_messenger.send_messages_from_sorted_json_files()
