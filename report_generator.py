import pandas as pd

def generate_report(consolidated_df, output_file: str):
    """
    Génère un rapport récapitulatif des stocks.
    """
    rapport_global = {
        'Nombre total de produits': len(consolidated_df),
        'Nombre de catégories': consolidated_df['categorie'].nunique(),
        'Valeur totale du stock': (consolidated_df['quantite'] * consolidated_df['prix_unitaire']).sum(),
        'Produit le plus cher': consolidated_df.loc[consolidated_df['prix_unitaire'].idxmax(), 'nom'],
        'Produit le moins cher': consolidated_df.loc[consolidated_df['prix_unitaire'].idxmin(), 'nom'],
    }

    rapport_par_categorie = consolidated_df.groupby('categorie').agg({
        'nom': 'count',
        'quantite': 'sum',
        'prix_unitaire': ['mean', 'min', 'max']
    })
    rapport_par_categorie.columns = ['Nombre de produits', 'Quantité totale', 'Prix moyen', 'Prix min', 'Prix max']

    if output_file.endswith('.xlsx'):
        with pd.ExcelWriter(output_file) as writer:
            pd.DataFrame.from_dict(rapport_global, orient='index', columns=['Valeur']).to_excel(writer, sheet_name='Rapport Global')
            rapport_par_categorie.to_excel(writer, sheet_name='Par Catégorie')
    else:
        pd.DataFrame.from_dict(rapport_global, orient='index', columns=['Valeur']).to_csv(output_file + '_global.csv')
        rapport_par_categorie.to_csv(output_file + '_categories.csv')

    print(f"Rapport généré : {output_file}")
