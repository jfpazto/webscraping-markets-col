from abc import ABC, abstractmethod
from dto.producto_dto import ProductoDTO


class BaseAdapter(ABC):
    @abstractmethod
    def adapt(self, raw_data, exchange_rate, store_url, currency) -> ProductoDTO:
        pass
