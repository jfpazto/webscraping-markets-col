from batch.base_batch import BaseBatch
from service.olimpica_service import OlimipicaService
import pandas as pd


class OlimpicaBatch(BaseBatch):
    def __init__(self):
        self.olimpica_service = OlimipicaService
        super().__init__("olimpica")

    def run_service(self) -> pd.DataFrame:
        try:
            service = self.olimpica_service.extrae_productos_olimpica()
            return pd.DataFrame(service)
        except Exception as e:
            print(f"Error al ejecutar el batch de Olimpica: {e}")
