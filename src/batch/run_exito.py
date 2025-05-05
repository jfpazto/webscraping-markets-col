from batch.base_batch import BaseBatch
from service.exito_service import ExitoService
import pandas as pd


class ExitoBatch(BaseBatch):
    def __init__(self):
        self.exito_service = ExitoService()
        super().__init__("exito")

    def run_service(self) -> pd.DataFrame:
        try:
            service = self.exito_service.retorna_productos_exito()
            return pd.DataFrame(service)
        except Exception as e:
            print(f"Error al ejecutar el batch de Falabella: {e}")
