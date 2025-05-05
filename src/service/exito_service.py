from processors.exito_processors import ExitoProcessor
import sys


class ExitoService:
    def __init__(self):
        self.processor = ExitoProcessor()

    def retorna_productos_exito(self):
        try:
            productos = self.processor.mapeo_productos()

            return productos
        except Exception as e:
            print(f"Error al obtener productos de Exito: {e}")
            return None
