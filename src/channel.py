from googleapiclient.discovery import build

import os
import json

class Channel:
    """Класс для ютуб-канала"""

    @classmethod
    def get_service(cls):
        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('API_KEY')

        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)

        return youtube

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.youtube=Channel.get_service()

        # channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        items_list=self.channel.get('items')
        snippet_dct=items_list[0].get('snippet')
        statistics_dct = items_list[0].get('statistics')

        self.title=snippet_dct.get('title')  # вДудь
        self.description = snippet_dct.get('description')
        self.video_count=statistics_dct.get('videoCount')  # 163 (может уже больше)
        self.subscriber_count = statistics_dct.get('subscriberCount')
        self.view_count = statistics_dct.get('viewCount')
        self.url=snippet_dct.get('customUrl')  # https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA


    def print_info(self, json_object='') -> None:
        """Выводит в консоль информацию о канале."""
        """Выводит словарь в json-подобном удобном формате с отступами"""
        if json_object != "":
            print(json.dumps(json_object, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self,json_name):
        prop_dct={}
        prop_dct["channel_id"]=self.__channel_id
        prop_dct["title"]=self.title
        prop_dct["url"]=self.url
        prop_dct["subscriber_count"]=self.subscriber_count
        prop_dct["video_count"]=self.video_count
        prop_dct["view_count"]=self.view_count

        json_object = json.dumps(prop_dct, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(json_name, "w", encoding='utf8') as outfile:
            outfile.write(json_object)
            #json.dump(prop_dct,  outfile, ensure_ascii=False)

    @property
    def channel_id(self):
        return self.__channel_id

    #магические методы
    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)