from processors.falabella_processors import FalabellaProccessor


class FalabellaService:
    def __init__(self):
        self.proccessor_falabella = FalabellaProccessor()

    def retorna_productos_falabella(self):
        try:
            return self.proccessor_falabella.all_products()
        except Exception as e:
            print(f"Error al obtener productos de Falabella: {e}")
            return None
