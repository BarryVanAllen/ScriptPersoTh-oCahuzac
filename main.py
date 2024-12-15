from data_loader import DataLoader
from search import SearchEngine
from report_generator import ReportGenerator
import argparse


def main():
    parser = argparse.ArgumentParser(description="Outil de gestion des stocks.")
    parser.add_argument('--directory', '-d', required=True, help="Dossier contenant les fichiers CSV.")
    parser.add_argument('--search', '-s', nargs=2, metavar=('field', 'value'),
                        help="Rechercher un produit (champ, valeur).")
    parser.add_argument('--report', '-r', metavar='output_file', help="Générer un rapport résumé.")

    args = parser.parse_args()

    # Étape 1 : Charger les fichiers CSV
    loader = DataLoader(args.directory)
    loader.load_csv_files()
    data = loader.get_data()
    if not data:
        print("Aucune donnée trouvée dans les fichiers CSV.")
        return

    # Étape 2 : Effectuer une recherche (optionnel)
    if args.search:
        field, value = args.search
        search_engine = SearchEngine(data)
        results = search_engine.search(field, value)
        if results:
            print(f"Résultats trouvés ({len(results)} lignes) :")
            for row in results:
                print(row)
        else:
            print("Aucun résultat trouvé.")

    # Étape 3 : Générer un rapport (optionnel)
    if args.report:
        report_generator = ReportGenerator(data)
        report_generator.generate_summary(args.report)


if __name__ == '__main__':
    main()
