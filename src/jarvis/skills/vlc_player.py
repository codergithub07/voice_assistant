"""VLC Media Player control via D-Bus MPRIS and file system."""
import difflib
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List

from jarvis.config import DEFAULT_MEDIA_DIR

class VLCController:
    """Controls VLC media playback using D-Bus MPRIS and process launching."""

    def __init__(self, media_dir: Optional[Path] = None):
        self.media_dir = Path(media_dir) if media_dir else DEFAULT_MEDIA_DIR

    def _get_mpris_interface(self):
        """Retrieve VLC's D-Bus MPRIS Player interface."""
        try:
            import dbus
            session_bus = dbus.SessionBus()
            vlc_object = session_bus.get_object("org.mpris.MediaPlayer2.vlc", "/org/mpris/MediaPlayer2")
            return dbus.Interface(vlc_object, "org.mpris.MediaPlayer2.Player")
        except Exception as e:
            print(f"[VLC Warning] D-Bus MPRIS unavailable or VLC is not running: {e}")
            return None

    def play_pause(self) -> bool:
        """Toggle play/pause on active VLC session."""
        interface = self._get_mpris_interface()
        if interface:
            interface.PlayPause()
            return True
        return False

    def next_track(self) -> bool:
        """Skip to next track."""
        interface = self._get_mpris_interface()
        if interface:
            interface.Next()
            return True
        return False

    def previous_track(self) -> bool:
        """Skip to previous track."""
        interface = self._get_mpris_interface()
        if interface:
            interface.Previous()
            return True
        return False

    def stop(self) -> bool:
        """Stop playback."""
        interface = self._get_mpris_interface()
        if interface:
            interface.Stop()
            return True
        return False

    def open_media(self, file_path: str) -> bool:
        """Launch VLC asynchronously with specified media file."""
        vlc_bin = shutil.which("vlc") or "/usr/bin/vlc"
        if not os.path.exists(file_path):
            print(f"[VLC Error] Media file not found: {file_path}")
            return False

        try:
            env = os.environ.copy()
            # Non-blocking launch so assistant doesn't freeze
            subprocess.Popen(
                [vlc_bin, file_path],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"[VLC] Launched: {file_path}")
            return True
        except Exception as e:
            print(f"[VLC Error] Failed to launch VLC: {e}")
            return False

    def find_best_matching_media(self, query: str) -> Tuple[Optional[str], float]:
        """Find best matching file in media directory using fuzzy comparison."""
        if not self.media_dir.exists():
            return None, 0.0

        best_match = None
        best_score = 0.0
        query_clean = query.lower().strip()

        for file_name in os.listdir(self.media_dir):
            file_clean = file_name.lower()
            score = difflib.SequenceMatcher(None, query_clean, file_clean).ratio()
            if score > best_score:
                best_score = score
                best_match = file_name

        return best_match, best_score

    def play_by_query(self, query: str) -> Optional[str]:
        """Search and play a video/song matching query."""
        best_match, score = self.find_best_matching_media(query)
        if best_match and score >= 0.25:
            full_path = str(self.media_dir / best_match)
            if self.open_media(full_path):
                return f"Playing {best_match}"
        return f"Could not find any media matching '{query}'"
