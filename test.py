import unittest
import pandas as pd
import os
import logging
from unittest.mock import patch, MagicMock
from stock_management import consolidate_csv, search_inventory
from report_generator import generate_report

class TestStockManagement(unittest.TestCase):

    @patch('stock_management.os.listdir')
    @patch('stock_management.os.path.exists')
    @patch('stock_management.pd.read_csv')
    def test_consolidate_csv(self, mock_read_csv, mock_exists, mock_listdir):
        # Mock the existence of the input directory and CSV files
        mock_exists.return_value = True
        mock_listdir.return_value = ['file1.csv', 'file2.csv']
        mock_read_csv.side_effect = [
            pd.DataFrame({'nom': ['item1', 'item2'], 'quantite': [10, 20], 'prix_unitaire': [1.0, 2.0]}),
            pd.DataFrame({'nom': ['item3', 'item4'], 'quantite': [30, 40], 'prix_unitaire': [3.0, 4.0]})
        ]

        # Test the consolidation function
        df = consolidate_csv('dummy_dir')

        # Verify the results
        self.assertEqual(len(df), 4)
        self.assertIn('categorie', df.columns)
        self.assertListEqual(df['categorie'].tolist(), ['file1', 'file1', 'file2', 'file2'])

    @patch('stock_management.consolidate_csv')
    def test_search_inventory(self, mock_consolidate_csv):
        # Mock the consolidated DataFrame
        mock_consolidate_csv.return_value = pd.DataFrame({
            'nom': ['item1', 'item2', 'item3'],
            'quantite': [10, 20, 30],
            'prix_unitaire': [1.0, 2.0, 3.0]
        })

        # Test the search function with various criteria
        df = search_inventory('dummy_dir', nom='item1', quantite=15, prix_unitaire=1.5)
        self.assertEqual(len(df), 0)  # No item meets all criteria

        df = search_inventory('dummy_dir', nom='item1')
        self.assertEqual(len(df), 1)
        self.assertEqual(df['nom'].iloc[0], 'item1')

        df = search_inventory('dummy_dir', quantite=15)
        self.assertEqual(len(df), 2)
        self.assertListEqual(df['nom'].tolist(), ['item2', 'item3'])

        df = search_inventory('dummy_dir', prix_unitaire=1.5)
        self.assertEqual(len(df), 2)
        self.assertListEqual(df['nom'].tolist(), ['item2', 'item3'])

    @patch('report_generator.pd.ExcelWriter')
    @patch('os.path.exists', return_value=True)
    def test_generate_report_excel(self, mock_exists, mock_ExcelWriter):
        # Setup mock DataFrame and ExcelWriter
        df = pd.DataFrame({'nom': ['item1'], 'quantite': [10], 'prix_unitaire': [1.0]})
        mock_writer = MagicMock()
        mock_ExcelWriter.return_value.__enter__.return_value = mock_writer

        # Test the report generation function for Excel
        with self.assertLogs(level='INFO') as log:
            generate_report(df, 'report.xlsx')
            self.assertIn("INFO:root:Fichier de rapport généré : report.xlsx", log.output)

        # Verify the Excel file save call
        self.assertTrue(mock_writer.save.called)

    @patch('os.path.exists', return_value=True)
    def test_generate_report_csv(self, mock_exists):
        # Setup mock DataFrame
        df = pd.DataFrame({'nom': ['item1'], 'quantite': [10], 'prix_unitaire': [1.0]})

        # Test the report generation function for CSV
        output_file = 'report'
        with self.assertLogs(level='INFO') as log:
            generate_report(df, output_file)
            self.assertIn(f"INFO:root:Fichier de rapport généré en CSV : {output_file}_global.csv et {output_file}_categories.csv", log.output)
            self.assertIn(f"INFO:root:Le fichier {output_file}_global.csv existe bien.", log.output)
            self.assertIn(f"INFO:root:Le fichier {output_file}_categories.csv existe bien.", log.output)

if __name__ == '__main__':
    unittest.main()
