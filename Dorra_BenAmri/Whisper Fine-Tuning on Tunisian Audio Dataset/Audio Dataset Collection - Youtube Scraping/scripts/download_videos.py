import os
import subprocess
import sys
import re

def safe_filename(name: str) -> str:
    """
    Removes characters that are invalid in Windows filenames.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def download_tedx_videos():
    # --- Detect project paths ---
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(scripts_dir, ".."))
    urls_file = os.path.join(project_root, "data_raw", "TEDxTN_URLS.txt")
    output_dir = os.path.join(project_root, "data_raw", "audio_full")

    # --- Create output dir ---
    os.makedirs(output_dir, exist_ok=True)

    print(f"📥 Reading URLs from: {urls_file}")

    # --- Read all lines ---
    with open(urls_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Python executable (inside venv)
    python_exe = sys.executable

    # --- Process each line ---
    for line in lines:
        line = line.strip()

        # Skip empty or comment lines
        if not line or line.startswith("#"):
            continue

        # Format: URL + optional filename
        parts = line.split(maxsplit=1)
        url = parts[0]

        if len(parts) > 1:
            raw_name = safe_filename(parts[1])
        else:
            raw_name = "%(title)s"

        print(f"\n⏳ Downloading:\n{url}\n→ as {raw_name}")

        # yt-dlp command using python -m yt_dlp
        cmd = [
            python_exe, "-m", "yt_dlp",
            "-f", "bestaudio/best",
            "-o", os.path.join(output_dir, raw_name + ".%(ext)s"),
            url
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"❌ ERROR downloading: {url}")
        else:
            print("✅ Download completed")

    print("\n🎉 All downloads finished successfully!")

if __name__ == "__main__":
    download_tedx_videos()