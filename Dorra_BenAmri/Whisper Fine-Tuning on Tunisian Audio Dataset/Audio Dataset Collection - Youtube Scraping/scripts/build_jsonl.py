import csv
import json
import os

def find_audio_file_by_index(index, dataset_type):
    """
    This function generates the file name for each dataset based on the index.
    It assumes files are named sequentially like train_000000.wav, test_000000.wav, etc.
    """
    if dataset_type == 'train':
        return f"train_{index:06d}.wav"
    elif dataset_type == 'test':
        return f"test_{index:06d}.wav"
    elif dataset_type == 'dev':
        return f"dev_{index:06d}.wav"
    else:
        raise ValueError("Invalid dataset type")

def create_jsonl_from_csv(csv_file_path, dataset_type, output_jsonl_path, audio_base_path):
    """
    This function reads the CSV file, processes each row, and creates a corresponding JSONL file.
    It only includes the audio file and transcription if the audio file exists.
    """
    # Open the CSV file and read its contents
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        # Open the output JSONL file for writing
        with open(output_jsonl_path, mode='w', encoding='utf-8') as jsonl_file:
            for index, row in enumerate(reader):
                # Find the audio file corresponding to the index
                audio_filename = find_audio_file_by_index(index, dataset_type)
                
                # Construct the correct path for the audio file within its corresponding subdirectory (train, dev, or test)
                audio_path = os.path.join(audio_base_path, dataset_type, audio_filename)

                # Normalize the path (to handle backslashes in Windows paths)
                audio_path = os.path.normpath(audio_path)

                # Check if the audio file exists
                if os.path.exists(audio_path):
                    # Prepare the JSON object for the row
                    json_entry = {
                        "audio": audio_path.replace("\\", "/"),  # Ensure the path is in Unix-style format
                        "text": row['transcription']  # 'text' field is now 'transcription'
                    }
                    # Write the JSON entry as a line in the JSONL file
                    jsonl_file.write(json.dumps(json_entry, ensure_ascii=False) + "\n")
                else:
                    print(f"Warning: Audio file {audio_path} not found. Skipping entry.")

    print(f"JSONL file created at {output_jsonl_path}")

# Paths to the CSV files and output JSONL files
train_csv = 'C:/Users/dorra/Documents/4IA/Projet 4IA/tedX/whisper-medical-project/data_raw/train.csv'
test_csv = 'C:/Users/dorra/Documents/4IA/Projet 4IA/tedX/whisper-medical-project/data_raw/test.csv'
dev_csv = 'C:/Users/dorra/Documents/4IA/Projet 4IA/tedX/whisper-medical-project/data_raw/dev.csv'

# Output paths for JSONL files
train_jsonl = 'C:/Users/dorra/Documents/4IA/Projet 4IA/tedX/whisper-medical-project/data_processed/train.jsonl'
test_jsonl = 'C:/Users/dorra/Documents/4IA/Projet 4IA/tedX/whisper-medical-project/data_processed/test.jsonl'
dev_jsonl = 'C:/Users/dorra/Documents/4IA/Projet 4IA/tedX/whisper-medical-project/data_processed/valid.jsonl'

# Base path for the audio files (correct path without the duplicate 'data_processed')
audio_base_path = "C:/Users/dorra/Documents/4IA/Projet 4IA/tedX/whisper-medical-project/data_processed/segments"

# Create the JSONL files for each dataset
create_jsonl_from_csv(train_csv, 'train', train_jsonl, audio_base_path)
create_jsonl_from_csv(test_csv, 'test', test_jsonl, audio_base_path)
create_jsonl_from_csv(dev_csv, 'dev', dev_jsonl, audio_base_path)