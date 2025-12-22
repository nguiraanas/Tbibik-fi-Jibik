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

def create_jsonl_file(csv_rows, split_name, output_jsonl_file):
    # Create the JSONL file for a specific split (train, dev, or test)
    with open(output_jsonl_file, "w", encoding="utf-8") as jsonl_file:
        for row in tqdm(csv_rows, desc=f"Creating {split_name}.jsonl"):
            base_name = row["audio_filename"].strip()
            start_time = float(row["start_time"])
            end_time = float(row["end_time"])
            transcription = row["transcription"].strip()

            # Build the relative path for the audio file
            audio_path = os.path.join("data_processed", "segments", split_name, f"{split_name}_{row['audio_filename']}.wav")
            
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