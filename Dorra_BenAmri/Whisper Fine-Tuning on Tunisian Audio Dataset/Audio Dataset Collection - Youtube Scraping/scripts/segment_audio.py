import os
import csv
import subprocess
import sys
import time

def find_project_root():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(scripts_dir, ".."))

def load_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def match_audio_file(root_audio_dir, base_name):
    """
    Find audio file downloaded by yt-dlp that matches the CSV base filename.
    Looks for .webm, .m4a, .mp4, .wav etc.
    """
    possible_exts = [".webm", ".m4a", ".mp3", ".mp4", ".wav"]

    for ext in possible_exts:
        full_path = os.path.join(root_audio_dir, base_name + ext)
        if os.path.isfile(full_path):
            return full_path

    return None  # not found

def cut_audio_segment(ffmpeg_path, audio_in, start, end, audio_out, timeout=60):
    """
    Cut a segment from audio_in into audio_out using ffmpeg.
    Converts to 16kHz mono WAV (Whisper requirement).
    """
    cmd = [
        ffmpeg_path,
        "-i", audio_in,
        "-ss", str(start),
        "-to", str(end),
        "-ar", "16000",
        "-ac", "1",
        audio_out,
        "-y"
    ]

    try:
        # Start ffmpeg with a timeout
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"⏳ WARNING: Segment processing timed out: {audio_in} from {start}s to {end}s")
        return False
    except subprocess.CalledProcessError:
        print(f"⚠️ ERROR: FFmpeg failed on file {audio_in}.")
        return False
    return True

def process_split(split_name, csv_rows, audio_full_dir, output_dir, ffmpeg_path):
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n🎧 Processing split: {split_name}, {len(csv_rows)} segments")

    last_audio = None
    last_audio_file_loaded = None

    for idx, row in enumerate(csv_rows):
        base_name = row["audio_filename"].strip()
        start = float(row["start_time"])
        end = float(row["end_time"])

        # Only look for new audio if base changed
        if base_name != last_audio:
            audio_file = match_audio_file(audio_full_dir, base_name)
            if audio_file is None:
                print(f"⚠️ WARNING: Audio file for '{base_name}' not found, skipping.")
                continue

            last_audio = base_name
            last_audio_file_loaded = audio_file

            print(f"\n➡️ Using audio: {os.path.basename(audio_file)}")

        # Build output filename
        out_file = os.path.join(output_dir, f"{split_name}_{idx:06d}.wav")

        # Skip if the file already exists
        if os.path.exists(out_file):
            print(f"⏩ Skipping already processed segment: {out_file}")
            continue

        # Attempt to cut the audio segment
        if not cut_audio_segment(
            ffmpeg_path,
            last_audio_file_loaded,
            start,
            end,
            out_file,
            timeout=90  # 60 seconds timeout
        ):
            print(f"⏳ Skipping problematic segment {idx+1}/{len(csv_rows)}: {os.path.basename(out_file)}")
            continue

        print(f"   ✓ Segment {idx+1}/{len(csv_rows)} saved: {os.path.basename(out_file)}")

def main():
    root = find_project_root()

    # Paths
    csv_train = os.path.join(root, "data_raw", "train.csv")
    csv_dev = os.path.join(root, "data_raw", "dev.csv")
    csv_test = os.path.join(root, "data_raw", "test.csv")

    audio_full_dir = os.path.join(root, "data_raw", "audio_full")
    segments_root = os.path.join(root, "data_processed", "segments")

    # ffmpeg detection
    ffmpeg_path = "ffmpeg"  # works on Windows if ffmpeg is in PATH
    print(f"🔎 Using ffmpeg executable: {ffmpeg_path}")

    # Load CSV splits
    train_rows = load_csv(csv_train)
    dev_rows = load_csv(csv_dev)
    test_rows = load_csv(csv_test)

    # Process all splits
    process_split("train", train_rows, audio_full_dir, os.path.join(segments_root, "train"), ffmpeg_path)
    process_split("dev", dev_rows, audio_full_dir, os.path.join(segments_root, "dev"), ffmpeg_path)
    process_split("test", test_rows, audio_full_dir, os.path.join(segments_root, "test"), ffmpeg_path)

    print("\n🎉 All audio segments generated successfully!")

if __name__ == "__main__":
    main()