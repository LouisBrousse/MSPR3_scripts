import pandas as pd
import os
import re

# === Répertoire contenant tous les fichiers CSV à traiter ===
input_folder = "election_presidentielles"

# === Lister tous les fichiers CSV ===
csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

for filename in csv_files:
    match = re.match(r"(.+?)_(\d{4})_communes_(T\d).csv", filename)
    if not match:
        print(f"❌ Fichier ignoré (nom non reconnu) : {filename}")
        continue

    type_elec, annee, tour = match.groups()
    input_path = os.path.join(input_folder, filename)
    output_filename = filename.replace(".csv", "_normalise.csv")
    output_path = os.path.join(input_folder, output_filename)

    try:
        df = pd.read_csv(input_path, sep=";", encoding="latin1")

        fixed_columns = df.columns[:15]
        candidate_columns = df.columns[15:]
        candidate_blocks = [candidate_columns[i:i+6] for i in range(0, len(candidate_columns), 6)]

        normalized_rows = []

        for block in candidate_blocks:
            temp = df[fixed_columns.tolist() + block.tolist()].copy()
            temp.columns = list(fixed_columns) + ["Sexe", "Nom", "Prénom", "Voix", "% Voix/Ins", "% Voix/Exp"]
            temp["type_election"] = type_elec
            temp["annee"] = annee
            temp["tour"] = tour
            normalized_rows.append(temp)

        normalized_df = pd.concat(normalized_rows, ignore_index=True)
        normalized_df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

        print(f"✅ Fichier traité : {filename} → {output_filename}")
    
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {filename} : {e}")
