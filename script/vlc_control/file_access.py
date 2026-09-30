import subprocess
import os

def open_vlc(video_file):
    """
    Opens a video file in VLC Media Player.
    
    Parameters:
    video_file (str): Full path to the video file.
    """
    
    try:
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu"
        # Launch VLC with the specified video file.
        subprocess.run(["/usr/bin/vlc", video_file], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Opened video: {video_file}")
    except subprocess.CalledProcessError as e:
        print("Failed to open VLC:", e)


# test video path: /media/tony/ddrive/Movies/Deadpool.&.Wolverine.2024.1080p.BluRay.Hindi.5.1.mkv
