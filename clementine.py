import dbus
from track import Track


class Clementine:
    def __init__(self):
        session_bus = dbus.SessionBus()
        self.player = session_bus.get_object('org.mpris.clementine', '/Player')
        self.track_list = session_bus.get_object('org.mpris.clementine', '/TrackList')

    def add_track(self, filename, run):
        self.track_list.AddTrack(filename, run)

    def play(self):
        self.player.Play()

    def play_num(self, num):
        self.track_list.PlayTrack(num)

    def pause(self):
        self.player.Pause()

    def volume_up(self, value):
        self.player.VolumeUp(int(value))

    def volume_down(self, value):
        self.player.VolumeDown(int(value))

    def get_volume(self):
        return str(self.player.VolumeGet())

    def get_track_list(self):
        tracks = []
        length = int(self.track_list.GetLength())
        for i in range(0, length):
            metadata = self.track_list.GetMetadata(i)
            tracks.append(self.track_from_metadata(metadata, i))
        return tracks

    def get_current_track_num(self):
        return int(self.track_list.GetCurrentTrack())

    @staticmethod
    def track_from_metadata(metadata, num):
        title = metadata['title'].encode('utf-8')
        return Track(num, title)