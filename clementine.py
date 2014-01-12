import dbus


class Clementine:

    def __init__(self):
        session_bus = dbus.SessionBus()
        player = session_bus.get_object('org.mpris.clementine', '/Player')
        self.player_iface = dbus.Interface(player, dbus_interface='org.freedesktop.MediaPlayer')

        track_list = session_bus.get_object('org.mpris.clementine', '/TrackList')
        #self.track_iface = dbus.Interface(track_list, dbus_interface='org.freedesktop.MediaPlayer')

    def add_track(self, filename, run):
        self.track_list.AddTrack(filename, run)
