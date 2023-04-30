import isodate
from src.channel import Channel
import datetime
import time

class PlayList(Channel):
    def __init__(self, playlist_id: str) -> None:
        self.youtube = Channel.get_service()

        self.playlist = self.youtube.playlists().list(id=playlist_id,
                                     part='contentDetails,snippet,status',
                                     ).execute()

        #self.print_info(self.playlist)
        #self.playlist_dct=json.loads(self.playlist)

        self.title=self.playlist["items"][0]["snippet"]['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

        playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails, snippet',
                                                       maxResults=50,
                                                       ).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        #print(video_ids)

        '''
        вывести длительности видеороликов из плейлиста
        docs: https://developers.google.com/youtube/v3/docs/videos/list
        '''
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        self.total_seconds=0.0
        likes_count = 0

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            video_duration = isodate.parse_duration(iso_8601_duration)
            duration_list=str(video_duration).split(':')
            self.total_seconds += datetime.timedelta(hours=int(duration_list[0]),minutes=int(duration_list[1]),seconds=int(duration_list[2])).total_seconds()

            if likes_count < int(video['statistics']['likeCount']):
                likes_count = int(video['statistics']['likeCount'])
                self.best_video_id=video['id']

        self.duration = datetime.timedelta(seconds=self.total_seconds)

    @property
    def total_duration(self):
        return self.duration

    def show_best_video(self):
        return f"https://youtu.be/{self.best_video_id}"
