import unittest
import pandas as pd
import os
from stock_management import consolidate_csv, search_inventory  # Import des fonctions modifiées
from report_generator import generate_report
from main import main

class TestConsolidateCsvs(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_csv_dir"
        self.output_file = "consolidated.csv"
        os.makedirs(self.test_dir, exist_ok=True)

        self.file1_content = "nom,quantite,prix_unitaire\nbanane,2,1.99\npomme,1,0.99\n"
        self.file2_content = "nom,quantite,prix_unitaire\ncarotte,5,0.99\ncourgette,3,2.99\n"
        self.file3_empty = ""
        self.file4_random = "id,toto,param\ncarotte,5,0.99\ncourgette,3,2.99\n"

        with open(os.path.join(self.test_dir, "file1.csv"), "w") as f1, \
                open(os.path.join(self.test_dir, "file2.csv"), "w") as f2, \
                open(os.path.join(self.test_dir, "file3.csv"), "w") as f3:
            f1.write(self.file1_content)
            f2.write(self.file2_content)
            f3.write(self.file3_empty)

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    def test_ok(self):
        # Test with valid files
        consolidated_df = consolidate_csv(self.test_dir)  # Appel direct à la fonction
        self.assertEqual(len(consolidated_df), 5)  # 2 rows from file1 + 2 rows from file2
        self.assertEqual(consolidated_df.iloc[0]["nom"], "banane")

    def test_empty_file(self):
        # Test with empty file
        with open(os.path.join(self.test_dir, "file3.csv"), "w") as f:
            f.write("")
        consolidated_df = consolidate_csv(self.test_dir)  # Appel direct à la fonction
        self.assertEqual(len(consolidated_df), 4)  # Only 4 rows from file1 and file2

    def test_random_file(self):
        # Test with a random file structure (non-CSV)
        with open(os.path.join(self.test_dir, "file4.csv"), "w") as f:
            f.write(self.file4_random)
        consolidated_df = consolidate_csv(self.test_dir)  # Appel direct à la fonction
        self.assertEqual(len(consolidated_df), 5)  # It should ignore non-CSV content (file4.csv)

    def test_not_file(self):
        # Test if there are no CSV files in the directory
        # Supprime tous les fichiers CSV, mais garde le répertoire
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))

        # Assurez-vous qu'aucun fichier CSV n'est présent
        self.assertEqual(len(os.listdir(self.test_dir)), 0)

        # Attendez-vous à ce que le DataFrame retourné soit vide
        consolidated_df = consolidate_csv(self.test_dir)  # Appel direct à la fonction
        self.assertEqual(len(consolidated_df), 0)  # Aucun fichier CSV trouvé, donc pas de données à consolider

class TestSearch(unittest.TestCase):
    def setUp(self):
        # Mock CSV content
        self.csv_content = """nom,quantite,prix_unitaire
pc,2,500.99
ecran,1,100.99
"""
        # Create a temporary file for testing
        self.test_file = "test_search.csv"
        with open(self.test_file, "w") as file:
            file.write(self.csv_content)

    def tearDown(self):
        # Remove the temporary file after tests
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_ok(self):
        # Test for valid query
        result = search_inventory(self.test_file, nom="pc")
        self.assertIsNotNone(result)
        self.assertEqual(result.iloc[0]["nom"], "pc")

    def test_no_result(self):
        # Test for no matching result
        result = search_inventory(self.test_file, nom="table")
        self.assertEqual(len(result), 0)

    def test_invalid_column(self):
        # Test for invalid column
        result = search_inventory(self.test_file, nom="rouge")
        self.assertEqual(len(result), 0)

    def test_file_not_found(self):
        # Test for file not found
        result = search_inventory("fichier_inexistant.csv", nom="pc")
        self.assertEqual(result, "Fichier introuvable.")

class TestGenerateReport(unittest.TestCase):
    def setUp(self):
        # Mock CSV content
        self.csv_content = """nom,quantite,prix_unitaire
pc,2,500.99
ecran,1,100.99
"""
        # Create a temporary file for testing
        self.test_file = "test_generateReport.csv"
        self.output_file = "test_report.xlsx"
        with open(self.test_file, "w") as file:
            file.write(self.csv_content)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_ok(self):
        # Test generating a report successfully
        consolidated_df = pd.read_csv(self.test_file)
        generate_report(consolidated_df, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def test_file_not_found(self):
        # Test generating a report with a non-existent file
        result = generate_report("fichier_inexistant.csv", self.output_file)
        self.assertEqual(result, "Fichier introuvable.")

if __name__ == "__main__":
    unittest.main()
