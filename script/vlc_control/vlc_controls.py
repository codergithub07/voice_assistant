import dbus
import time

def get_vlc_interface():
    # Connect to the D-Bus session bus
    session_bus = dbus.SessionBus()
    # Access VLC's MPRIS interface (ensure VLC is running)
    try:
        vlc_object = session_bus.get_object("org.mpris.MediaPlayer2.vlc", "/org/mpris/MediaPlayer2")
    except dbus.DBusException:
        print("VLC is not running or D-Bus interface is not enabled.")
        exit(1)
    # Get the player interface
    return dbus.Interface(vlc_object, "org.mpris.MediaPlayer2.Player")

def play_pause():
    interface = get_vlc_interface()
    interface.PlayPause()
    print("Toggled play/pause.")

def next_track():
    interface = get_vlc_interface()
    interface.Next()
    print("Skipped to next track.")

def previous_track():
    interface = get_vlc_interface()
    interface.Previous()
    print("Went to previous track.")

if __name__ == "__main__":
    # Example usage: toggle play, wait 5 seconds, skip track, wait 5 seconds, then pause.
    play_pause()
    time.sleep(5)
    next_track()
    time.sleep(5)
    play_pause()
