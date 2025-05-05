import pandas as pd

# Lecture du fichier CSV en précisant le séparateur (;)
df = pd.read_csv("elections.csv", sep=";", encoding="latin1")

# Séparer les colonnes fixes (commune, votants...) des colonnes variables (candidats)
# On suppose que les 15 premières colonnes sont fixes (jusqu'à "% Exp/Vot")
fixed_columns = df.columns[:15]

# Le reste des colonnes est structuré en blocs de 6 (Sexe, Nom, Prénom, Voix, % Voix/Ins, % Voix/Exp)
candidate_columns = df.columns[15:]

# On regroupe les colonnes de chaque candidat en une liste de tuples
candidate_blocks = [candidate_columns[i:i+6] for i in range(0, len(candidate_columns), 6)]

# Liste pour stocker les DataFrames normalisés
normalized_rows = []

for block in candidate_blocks:
    # Créer un DataFrame avec les colonnes fixes + ce bloc candidat
    temp = df[fixed_columns.tolist() + block.tolist()].copy()
    temp.columns = list(fixed_columns) + ["Sexe", "Nom", "Prénom", "Voix", "% Voix/Ins", "% Voix/Exp"]
    normalized_rows.append(temp)

# Concaténer tous les blocs
normalized_df = pd.concat(normalized_rows, ignore_index=True)

# Enregistrer le résultat dans un nouveau fichier CSV
normalized_df.to_csv("elections_normalise.csv", sep=";", index=False)

print("Fichier normalisé écrit dans 'elections_normalise.csv'")
print(f"✅ Fichier normalisé enregistré : ")

