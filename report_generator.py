import pandas as pd
import os
import logging


def generate_report(consolidated_df, output_file: str):
    """
    Génère un rapport récapitulatif des stocks, avec la catégorie extraite du nom du fichier.
    """
    try:
        category = os.path.splitext(os.path.basename(output_file))[0]

        rapport_global = {
            'Nom du fichier': output_file,
            'Catégorie': category,
            'Nombre total de produits': len(consolidated_df),
            'Valeur totale du stock': (consolidated_df['quantite'] * consolidated_df['prix_unitaire']).sum(),
        }

        rapport_par_categorie = pd.DataFrame({
            'Nom de catégorie': [category],
            'Quantité': [consolidated_df['quantite'].sum()],
        })

        if output_file.endswith('.xlsx'):
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                pd.DataFrame.from_dict(rapport_global, orient='index', columns=['Valeur']).to_excel(writer,
                                                                                                    sheet_name='Rapport Global')
                rapport_par_categorie.to_excel(writer, sheet_name='Par Catégorie')

                empty_df = pd.DataFrame()
                empty_df.to_excel(writer, sheet_name='Feuille Vide')

                workbook = writer.book
                workbook.active = workbook['Rapport Global']

            logging.info(f"Fichier de rapport généré : {output_file}")
        else:
            global_csv = f"{output_file}_global.csv"
            category_csv = f"{output_file}_categories.csv"
            pd.DataFrame.from_dict(rapport_global, orient='index', columns=['Valeur']).to_csv(global_csv)
            rapport_par_categorie.to_csv(category_csv)

            logging.info(f"Fichier de rapport généré en CSV : {global_csv} et {category_csv}")

            if os.path.exists(global_csv):
                logging.info(f"Le fichier {global_csv} existe bien.")
            else:
                logging.warning(f"Le fichier {global_csv} n'a pas été généré.")

            if os.path.exists(category_csv):
                logging.info(f"Le fichier {category_csv} existe bien.")
            else:
                logging.warning(f"Le fichier {category_csv} n'a pas été généré.")
    except Exception as e:
        logging.error(f"Erreur lors de la génération du rapport: {e}")

