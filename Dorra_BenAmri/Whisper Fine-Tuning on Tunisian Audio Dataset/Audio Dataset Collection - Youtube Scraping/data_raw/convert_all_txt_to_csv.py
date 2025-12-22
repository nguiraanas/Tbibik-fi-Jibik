import csv
import os
from pathlib import Path

# Dossier contenant les fichiers .txt
FOLDER = Path(".")

# Trouver tous les fichiers .txt du dossier
txt_files = list(FOLDER.glob("*.txt"))

print(f"Fichiers trouvés : {[f.name for f in txt_files]}")

for txt_file in txt_files:
    csv_file = txt_file.with_suffix(".csv")

    print(f"Conversion : {txt_file.name} → {csv_file.name}")

    with txt_file.open("r", encoding="utf-8") as fin, \
         csv_file.open("w", encoding="utf-8-sig", newline="") as fout:

        writer = csv.writer(fout)

        for i, line in enumerate(fin):
            line = line.strip()
            if not line:
                continue

            if i == 0:
                # Écrire l'en-tête tel quel
                writer.writerow([c.strip() for c in line.split(",")])
                continue

            # Séparer sur les 3 premières virgules seulement
            parts = line.split(",", 3)

            if len(parts) != 4:
                print(f"⚠️ Ligne suspecte dans {txt_file.name} : {line}")
                continue

            audio, start, end, transcript = parts

            audio = audio.strip()
            start = start.strip()
            end = end.strip()
            transcript = transcript.strip()

            # Ajouter des guillemets autour de la transcription
            transcript = f"\"{transcript}\""

            # Écrire la ligne CSV
            writer.writerow([audio, start, end, transcript])

print("\n🎉 Conversion terminée pour tous les fichiers .txt du dossier !")