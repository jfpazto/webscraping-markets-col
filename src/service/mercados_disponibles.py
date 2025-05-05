import json


class TiendasDisponibles:
    def __init__(self):
        self.tiendas = {
            1: "homecenter",
            2: "falabella",
            3: "alkosto",
            4: "exito",
            5: "ktronix",
            6: "mercadolibre",
            7: "olimpica",
        }

    def retorna_mercados_disponibles(self):
        return self.tiendas
