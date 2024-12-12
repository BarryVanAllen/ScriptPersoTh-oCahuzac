import os
import pandas as pd
from typing import Optional

def consolidate_csv(input_dir: str) -> pd.DataFrame:
    """
    Consolide tous les fichiers CSV du répertoire en un seul DataFrame.
    """
    all_dataframes = []

    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Le répertoire {input_dir} n'existe pas.")

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(input_dir, filename)
            try:
                df = pd.read_csv(filepath)
                df['categorie'] = filename[:-4]
                all_dataframes.append(df)
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {filename} : {e}")

    # Si aucun fichier CSV n'a été trouvé, retourner un DataFrame vide
    if not all_dataframes:
        return pd.DataFrame()  # Retourne un DataFrame vide

    consolidated_df = pd.concat(all_dataframes, ignore_index=True)
    consolidated_df.columns = [col.lower().strip() for col in consolidated_df.columns]

    # Normaliser les types des colonnes
    consolidated_df['quantite'] = pd.to_numeric(consolidated_df['quantite'], errors='coerce')
    consolidated_df['prix_unitaire'] = pd.to_numeric(consolidated_df['prix_unitaire'], errors='coerce')

    return consolidated_df


def search_inventory(input_dir: str,
                     nom: Optional[str] = None,
                     quantite: Optional[int] = None,
                     prix_unitaire: Optional[float] = None) -> pd.DataFrame:
    """
    Recherche des produits selon différents critères.
    """
    # Appel de la fonction consolidate_csv pour récupérer le DataFrame consolidé
    consolidated_df = consolidate_csv(input_dir)

    result = consolidated_df.copy()

    if nom:
        result = result[result['nom'].str.contains(nom, case=False, na=False)]

    if quantite is not None:
        result = result[result['quantite'] >= quantite]

    if prix_unitaire is not None:
        result = result[result['prix_unitaire'] >= prix_unitaire]

    return result
