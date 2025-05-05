from batch.base_batch import BaseBatch
from service.homecenter_service import HomecenterService
import pandas as pd


class HomeCenterBatch(BaseBatch):
    def __init__(self):
        self.homecenter_service = HomecenterService()
        super().__init__("homecenter")

    def run_service(self) -> pd.DataFrame:
        try:
            service = self.homecenter_service.obtener_productos()
            return pd.DataFrame(service)
        except Exception as e:
            print(f"Error al ejecutar el batch de Homecenter: {e}")
