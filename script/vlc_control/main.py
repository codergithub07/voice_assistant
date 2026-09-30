if __name__ == "__main__":
    import file_access
    import vlc_controls
    import time
    file_access.open_vlc("/media/tony/ddrive/Movies/Deadpool.&.Wolverine.2024.1080p.BluRay.Hindi.5.1.mkv")
    vlc_controls.play_pause()
    time.sleep(5)
    vlc_controls.next_track()
    time.sleep(5)
    vlc_controls.previous_track()