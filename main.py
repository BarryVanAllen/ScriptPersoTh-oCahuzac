import argparse
from stock_management import consolidate_csv, search_inventory
from report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description="Gestion des stocks")
    parser.add_argument("input_dir", help="Répertoire contenant les fichiers CSV")
    parser.add_argument("commande", choices=["recherche", "rapport"], help="Commande à exécuter")
    parser.add_argument("--nom", help="Nom du produit à rechercher")
    parser.add_argument("--quantite", type=int, help="Quantité minimale à rechercher")
    parser.add_argument("--prix_unitaire", type=float, help="Prix unitaire minimum à rechercher")
    parser.add_argument("--export", help="Fichier pour exporter les résultats de la recherche")
    parser.add_argument("--output", help="Fichier pour exporter le rapport")

    args = parser.parse_args()

    if args.commande == 'recherche':
        resultats = search_inventory(
            input_dir=args.input_dir,
            nom=args.nom,
            prix_unitaire=args.prix_unitaire,
            quantite=args.quantite
        )

        if args.export:
            resultats.to_csv(args.export, index=False)
            print(f"Résultats exportés vers {args.export}")
        else:
            print(resultats)

    elif args.commande == 'rapport':
        consolidated_df = consolidate_csv(args.input_dir)
        generate_report(consolidated_df, args.output)

if __name__ == '__main__':
    main()
