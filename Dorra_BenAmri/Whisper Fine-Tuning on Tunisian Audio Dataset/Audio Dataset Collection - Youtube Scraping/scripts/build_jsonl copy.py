import os
import json
import csv
from tqdm import tqdm

def find_project_root():
    # Detect the project root directory (the folder containing the scripts and data)
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(scripts_dir, ".."))

def load_csv(path):
    # Load the CSV file (train.csv, dev.csv, or test.csv)
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def map_audio_filename(base_name, index):
    """
    Maps the descriptive audio filename from CSV to the segmented filename (train_000000.wav).
    We assume the segments are named sequentially.
    """
    audio_filename_prefix = "train_"
    # Format the filename as train_000001.wav, train_000002.wav, etc.
    return f"{audio_filename_prefix}{index:06d}"  # Formats as "train_000001"

def create_jsonl_file(csv_rows, split_name, output_jsonl_file):
    """
    Create the JSONL file for a specific split (train, dev, or test).
    The function iterates over all rows in the CSV, processes them, and generates the JSONL format.
    """
    with open(output_jsonl_file, "w", encoding="utf-8") as jsonl_file:
        # Track how many times each audio file appears in the CSV
        audio_filename_counter = {}

        for row in tqdm(csv_rows, desc=f"Creating {split_name}.jsonl"):
            base_name = row["audio_filename"].strip()  # Extract the base name (What_I_can_do_in_Tunisia...)
            start_time = float(row["start_time"])     # Start time of the segment
            end_time = float(row["end_time"])         # End time of the segment
            transcription = row["transcription"].strip()  # Transcription text

            # Track how many times this base name has been encountered
            if base_name not in audio_filename_counter:
                audio_filename_counter[base_name] = 0
            audio_filename_counter[base_name] += 1

            # Generate the corresponding segment filename based on the counter (e.g., train_000001.wav, train_000002.wav)
            segment_filename = map_audio_filename(base_name, audio_filename_counter[base_name])

            # Construct the audio file path for each segment
            audio_path = os.path.join("data_processed", "segments", split_name, f"{segment_filename}.wav")
            
            # Construct the JSON object for each segment
            json_line = {
                "audio": audio_path,
                "text": transcription
            }

            # Write the JSON object as a line in the JSONL file
            jsonl_file.write(json.dumps(json_line, ensure_ascii=False) + "\n")
    print(f"✅ {split_name}.jsonl created!")

def main():
    # Get the project root directory
    root = find_project_root()

    # Paths to the CSV files (train.csv, dev.csv, test.csv)
    csv_train = os.path.join(root, "data_raw", "train.csv")
    csv_dev = os.path.join(root, "data_raw", "dev.csv")
    csv_test = os.path.join(root, "data_raw", "test.csv")

    # Load the CSV splits (train, dev, test)
    train_rows = load_csv(csv_train)
    dev_rows = load_csv(csv_dev)
    test_rows = load_csv(csv_test)

    # Create JSONL files for each split (train, dev, test)
    create_jsonl_file(train_rows, "train", os.path.join(root, "data_processed", "train.jsonl"))
    create_jsonl_file(dev_rows, "dev", os.path.join(root, "data_processed", "valid.jsonl"))
    create_jsonl_file(test_rows, "test", os.path.join(root, "data_processed", "test.jsonl"))

    print("\n🎉 JSONL files generated successfully!")

if __name__ == "__main__":
    main()
