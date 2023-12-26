import datetime
import json
import os
import time

from googleapiclient.discovery import build
import logging
from _youtube_notification_post_telegram import TelegramMessenger

logging.basicConfig(level=logging.DEBUG)


class YoutubeChannelMonitor:

    def __init__(self, key_file, data_dir, channel_list: list):
        self.key_file = key_file
        self.data_dir = data_dir
        self.channel_list: list = channel_list

        # Create the YouTube service
        self.youtube = self._create_youtube_service()

    def _create_youtube_service(self) -> object:
        # Load the service account credentials from the provided key file
        api_key = 'AIzaSyCBboIUP1LV4Vt82BRV8cN3qgwrf43LMYQ'
        # Build the YouTube service
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def get_channel_id(self, username: list) -> object:
        try:
            # Search for the channel using the username
            search_response = self.youtube.search().list(
                q=username,
                type='channel',
                part='id'
            ).execute()

            # Extract the channel ID from the search results
            if 'items' in search_response:
                channel_id = search_response['items'][0]['id']['channelId']
                return channel_id

        except Exception as e:
            print(f"Error: {e}")
            return None

    def _add_channels(self, _channel_list: object = None) -> list:
        if _channel_list is None:
            _channel_list = self.channel_list

        # Ensure _channel_list is not too long
        if len(_channel_list) > 5:
            print("Warning: List exceeds the limit for channels")
            _ch = _channel_list[:5]
        else:
            _ch = _channel_list

        _ch_id = []

        for ch in _ch:
            ch_id = self.get_channel_id(ch)
            _ch_id.append(ch_id)
        print(_ch_id)
        _v_ch = []
        for ch in _ch_id:
            youtube = self.youtube
            print("Stoppage-1")
            print(ch)
            response = youtube.channels().list(
                part='snippet',
                id=ch
            ).execute()
            print("Stoppage-2")
            if 'items' in response:
                print(ch)
                _v_ch.append(ch)
            else:
                print("Nothing inside the response try again")
                print(response)
                break
        return _v_ch

    def _fetch_latest_video(self, _ch_id: str):
        response=dict()
        print("Hello")
        try:
            response = self.youtube.search().list(
                channelId=_ch_id,
                order='date',
                maxResults=1,
                part='snippet'
            ).execute()
        except Exception as error:
            print("Error:", error)
            print("The Response:",response)

        if 'items' in response:
            print("Stoppage")
            video = response['items'][0]
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            return {
                'title': video_title,
                'url': video_url,
                'timestamp': datetime.datetime.now().isoformat()
            }

        else:
            print("Nothing in the response dict")
            return None

    def write_json(self):
        _ch = self._add_channels()
        if _ch is None:
            logging.info(f"Add channels, list empty")
        else:
            while True:
                try:
                    for _id in _ch:
                        latest_video = self._fetch_latest_video(_id)
                        telegrammessenger = TelegramMessenger(
                            bot_token='6520699737:AAHqnUlHw7VdGYuglehCll7pXC8VqBN1Q4Y', chat_id='@thehindutribune',
                            data_dir=None)
                        if latest_video:
                            telegrammessenger.send_message(latest_video['title'], latest_video['url'],
                                                       latest_video['timestamp'])
                        else:
                            message = "No youtube updates to send!"
                            telegrammessenger.send_message(message, None, None)

                        if latest_video:
                            # Write video details to a JSON file
                            filename = os.path.join(self.data_dir, f'{_id}_id.json')
                            with open(filename, 'w') as file:
                                json.dump(latest_video, file, indent=2)
                except Exception as e:
                    logging.info("Updating Latest Vid Info")
                time.sleep(7200)


# Example usage:
# monitor = YoutubeChannelMonitor(bot_token, key_file, data_dir, channel_list)
# monitor.write_json()

if __name__ == '__main__':
    Key = "movierequesthandler-8cdedebff56c.json"
    data_dir = 'data_files'
    dir_path = os.path.join(os.curdir, data_dir)
    print(dir_path)
    ch_list = ["@GovardhanMath","@IndicAcademy","@VedantaNY","@RMICGolpark","@ChinmayaChannel"]
    monitor = YoutubeChannelMonitor(Key, dir_path, ch_list)
    monitor._add_channels(ch_list)
    print("oops")
    monitor.write_json()
