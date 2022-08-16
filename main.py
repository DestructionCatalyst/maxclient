import requests
import sys
from abc import ABC, abstractmethod
from time import sleep
from datetime import datetime

LONG_DASH = "\u2014"
CHANNEL_HASH = "add441ad-4aaf-440f-9231-53a08eedd2eb"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
}
times = 0


def get_channel_data() -> dict:
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        global times
        from test import data
        times += 1
        # print(data[times - 1]["test"], file=sys.stderr)
        return data[times - 1]["test"]
    else:
        result = requests.get("https://maximum.ru/api/radio/current", headers=HEADERS)
        result.raise_for_status()
        return result.json()[CHANNEL_HASH]


class BaseTrack(ABC):
    @abstractmethod
    def format_as_playlist(self, time=None):
        pass

    @abstractmethod
    def format_as_current(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

class Track(BaseTrack):
    def __init__(self, track_data: dict):
        self.artist = track_data.get("artist") or track_data.get("song_artist")
        self.name = track_data.get("name")
        self.time = track_data.get("time")
        if self.time:
            self.time = datetime.strptime(self.time, "%Y-%m-%d %H:%M")
        self.id = track_data.get("id")

    def format_as_playlist(self, time=None):
        if not time and not self.time:
            raise ValueError("Cannot format this track as playlist track, please provide time parameter")
        time = self.time or time
        return f"{time.strftime('%H:%M')}\t{self.artist} {LONG_DASH} {self.name}\n"

    def format_as_current(self):
        return f"Now playing: {self.artist} {LONG_DASH} {self.name}\n"

    def __eq__(self, other):
        return isinstance(other, Track) and self.id == other.id


class NoTrack(BaseTrack):
    def format_as_playlist(self, time=None):
        return ""

    def format_as_current(self):
        return f"~~~ No music currently playing ~~~\n"

    def __eq__(self, other):
        return isinstance(other, NoTrack)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        CHANNEL_HASH = sys.argv[1]
    # if just launched:
    # load data
    channel_data = get_channel_data()
    # print playlist
    for track_dict in reversed(channel_data["playlist"][1:]):
        print(Track(track_dict).format_as_playlist(), end="")
    # print current track
    cur_track = Track(channel_data["current_track"])
    print(cur_track.format_as_current(), end="")
    cur_time = datetime.strptime(channel_data["playlist"][0]["time"], "%Y-%m-%d %H:%M")
    # each minute
    try:
        while True:
            sleep(60)
            # load data
            channel_data = get_channel_data()
            if channel_data["current_track"]:
                new_cur_track = Track(channel_data["current_track"])
            else:
                new_cur_track = NoTrack()
            # if current track changes
            if new_cur_track != cur_track:
                # re-print previous track as a part of a playlist
                sys.stdout.write("\033[F\033[K")
                print(f"{cur_track.format_as_playlist(cur_time)}", end="")
                # print new current track
                cur_track = new_cur_track
                print(cur_track.format_as_current(), end="")
                cur_time = datetime.now()
    except KeyboardInterrupt:
        exit(0)
