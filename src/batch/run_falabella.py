from batch.base_batch import BaseBatch
from service.falabella_service import FalabellaService
import pandas as pd


class FalabellaBatch(BaseBatch):
    def __init__(self):
        self.falabella_service = FalabellaService()
        super().__init__("falabella")

    def run_service(self) -> pd.DataFrame:
        try:
            service = self.falabella_service.retorna_productos_falabella()
            return pd.DataFrame(service)
        except Exception as e:
            print(f"Error al ejecutar el batch de Falabella: {e}")
