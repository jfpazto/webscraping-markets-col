from processors.olimpica_processors import OlimpicaProcessors


class OlimipicaService:
    def __init__(self):
        self.url = "wwww.olimpica.com"
        self.productos_olimpica = OlimpicaProcessors()

    def extrae_productos_olimpica(self):
        return self.productos_olimpica.procesa_productos()
