import os
import csv
from typing import List, Dict

class DataLoader:
    def __init__(self, directory: str):
        self.directory = directory
        self.data = []

    def load_csv_files(self) -> None:
        """Charge et consolide les fichiers CSV dans un seul tableau."""
        for filename in os.listdir(self.directory):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        self.data.append(row)

    def get_data(self) -> List[Dict]:
        """Renvoie les données consolidées."""
        return self.data
