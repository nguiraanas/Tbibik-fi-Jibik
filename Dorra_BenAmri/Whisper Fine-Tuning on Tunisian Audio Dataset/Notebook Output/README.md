# Notebook Training Outputs (Summary)

This folder contains the outputs generated during Whisper fine-tuning
using LoRA on a Tunisian Arabic speech dataset.

## Training checkpoints
- checkpoint-197
- checkpoint-394
- checkpoint-591

Each checkpoint includes:
- LoRA adapter weights
- optimizer and scheduler states
- training metadata (trainer_state.json)

## Final model
The final LoRA adapter was saved under:
- whisper-base-tunisian-lora/

Due to size constraints, the actual binary artifacts are not versioned.
They are available on Kaggle / Hugging Face.

This repository focuses on:
- data collection
- preprocessing
- training logic
- reproducibility