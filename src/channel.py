from googleapiclient.discovery import build
import os
import json

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        self.api_key: str = os.getenv('API_KEY')

        # создать специальный объект для работы с API
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

