from scrapers.falabella_scraper import FalabellaScraper
from adapters.falabella_adapter import FalabellaAdapter
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


class FalabellaProccessor:
    def __init__(self):
        self.scraper_falabella = FalabellaScraper()
        self.falabella_adapter = FalabellaAdapter()
        self.exchange_rate = 5000
        self.store_url = "www.falabella.com"
        self.currency = "COP"
        self.tecnologia = "tecnologia"
        self.electro_hogar = "electrohogar"

    def extrae_productos_falabella(self, page, categoria):
        if categoria == self.tecnologia:
            json_api_tecnologia = self.scraper_falabella.get_falabella_products(page)
        elif categoria == self.electro_hogar:
            json_api_tecnologia = (
                self.scraper_falabella.get_falabella_products_electrohogar(page)
            )
        return json_api_tecnologia

    def lista_productos_falabella(self, json_api_falabella):
        try:
            cantidad_producto = json_api_falabella["data"]["pagination"]["count"]
            print("Cantidad productos falabella: ", cantidad_producto)
            lista_productos_falabella = json_api_falabella["data"]["results"]
            products_falabella = []
            for producto in lista_productos_falabella:
                dto_producto = self.falabella_adapter.parse_raw_data(
                    producto, self.exchange_rate, self.store_url, self.currency
                )
                products_falabella.append(dto_producto)
            return products_falabella
        except Exception as e:
            print(f"Error al hacer el mapping inicial: {e}")

    def all_products(self):
        categorias = [self.tecnologia, self.electro_hogar]
        df_total = None

        def scrape_categoria(categoria):
            nonlocal df_total
            con = 1
            print("Scrapeando categoría:", categoria)
            while True:
                json_api_falabella = self.extrae_productos_falabella(con, categoria)
                if json_api_falabella == "":
                    break
                status = json_api_falabella[1]
                if status != 200:
                    print(
                        f"Status {status} recibido en página {con}, deteniendo scraping para esta categoría."
                    )
                    break
                data = self.lista_productos_falabella(json_api_falabella[0])
                if not data:
                    print(f"No se encontró data válida en página {con}")
                    break
                nuevo = pd.DataFrame(data)
                print("Página #:", con)
                if df_total is None:
                    df_total = nuevo
                else:
                    df_total = pd.concat([df_total, nuevo], ignore_index=True)
                con += 1

        # Usa ThreadPoolExecutor para procesar categorías en paralelo
        with ThreadPoolExecutor(max_workers=len(categorias)) as executor:
            executor.map(scrape_categoria, categorias)

        return df_total
