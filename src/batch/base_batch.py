from abc import ABC, abstractmethod
from datetime import datetime
import os
import pandas as pd


class BaseBatch(ABC):
    def __init__(self, tienda: str):
        self.tienda = tienda
        self.today = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join("output", self.tienda, self.today)
        os.makedirs(self.output_dir, exist_ok=True)

    @abstractmethod
    def run_service(self) -> pd.DataFrame:
        pass

    def save_to_csv(self, df: pd.DataFrame):
        filename = f"{self.tienda}_{self.today}.csv"
        path = os.path.join(self.output_dir, filename)
        df.to_csv(path, index=False)
        print(f"Archivo guardado en: {path}")

    def run(self):
        df = self.run_service()
        self.save_to_csv(df)
