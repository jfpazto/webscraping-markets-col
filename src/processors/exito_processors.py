from scrapers.exito_scraper import ExitoScraper
from scrapers.dollar_price import DollarPriceScraper
from datetime import date
from dto.producto_dto import ProductoDTO
from adapters.exito_adapter import ExitoAdapter
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


class ExitoProcessor:
    def __init__(self):
        self.store_url = "https://www.exito.com"
        self.currency = "COP"
        self.exchange_rate = (
            5000  # Puedes reemplazarlo con `retorna_precio_dolar()` si es dinámico
        )
        self.exito_scraper = ExitoScraper()

    def retorna_productos(self, page):
        try:
            return self.exito_scraper.get_exito_products(page)
        except Exception as e:
            print(f"Error al obtener productos de Exito: {e}")
            return None

    def mapeo_productos(self):
        df_total = None
        total_pages = 200  # Número total de páginas a recorrer
        max_workers = 10  # Número de hilos

        def scrape_page_range(start, end):
            nonlocal df_total
            for page in range(start, end + 1):
                print(f"Obteniendo productos de la página: {page}")
                productos = self.retorna_productos(page)
                if not productos:
                    print(
                        f"No se encontraron productos o el estado no es 200 en la página {page}"
                    )
                    break

                try:
                    list_products = productos["data"]["search"]["products"]["edges"]
                    print(
                        f"Cantidad de productos en la página {page}: {len(list_products)}"
                    )

                    if len(list_products) > 0:
                        nuevo = pd.DataFrame(self.procesa_productos(list_products))
                        if df_total is None:
                            df_total = nuevo
                        else:
                            df_total = pd.concat([df_total, nuevo], ignore_index=True)
                    else:
                        print(f"No se encontraron productos en la página {page}")
                        break

                except Exception as e:
                    print(f"Error al mapear productos en la página {page}: {e}")
                    break

        pages_per_worker = total_pages // max_workers
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    scrape_page_range,
                    i * pages_per_worker + 1,
                    (i + 1) * pages_per_worker,
                )
                for i in range(max_workers)
            ]
            for future in futures:
                future.result()
        return df_total

    def procesa_productos(self, productos):
        productos_exito = []
        exito_adapter = ExitoAdapter()
        for producto in productos:
            dto = exito_adapter.parse_raw_data(
                raw_data=producto,
                exchange_rate=self.exchange_rate,
                store_url=self.store_url,
                currency=self.currency,
            )
            if dto:
                productos_exito.append(dto)
        return productos_exito
