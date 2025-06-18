import os
import subprocess
from pathlib import Path

def access_windows_file(file_relative_path):
    # Define paths and device
    mount_point = Path("/media/ddrive")
    windows_device = "/dev/sda1"  # Replace with your partition
    file_path = mount_point / file_relative_path

    # Check if already mounted
    if not os.path.ismount(mount_point):
        try:
            # Create mount directory if it doesn't exist
            mount_point.mkdir(parents=True, exist_ok=True)
            
            # Mount the partition (requires sudo privileges)
            subprocess.run(
                ["sudo", "mount", "-t", "ntfs-3g", windows_device, str(mount_point)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Mounted Windows partition successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to mount: {e}")
            return None  # Or raise an exception

    # Access the file
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {file_path} not found!")
        return None

# Example usage
file_content = access_windows_file("example.txt")
if file_content:
    print(file_content)