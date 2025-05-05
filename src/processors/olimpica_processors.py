from scrapers.olimpica_scraper import OlimpicaScraper
from adapters.olimpica_adapter import OlimpicaAdapter
from utils.io_utils import url_encode, url_decode, base64_decode, base64_encode
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import pandas as pd


class OlimpicaProcessors:
    def __init__(self):
        self.url = "www.olimpica.com"
        self.olimpica_scraper = OlimpicaScraper()
        self.olimpica_adapter = OlimpicaAdapter()
        self.exchange_rate = 5000
        self.store_url = "www.olimpica.com"
        self.currency = "COP"

    def procesa_productos(self):
        try:
            url_decoded = self._decode_initial_url()
            df_total = pd.DataFrame()
            page_size = 10
            max_iterations = 80
            max_workers = 10

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(
                        self._fetch_page_data, url_decoded, start, page_size
                    )
                    for start in range(0, max_iterations * page_size, page_size)
                ]
                for future in as_completed(futures):
                    df_page = future.result()
                    df_total = pd.concat([df_total, df_page], ignore_index=True)
                    print(f"Longitud actual del DataFrame: {len(df_total)}")

            return df_total

        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
        except KeyError as e:
            print(f"Clave faltante en los datos: {e}")
        except Exception as e:
            print(f"Error al procesar productos: {e}")
        return None

    def _decode_initial_url(self):
        try:
            return json.loads(
                url_decode(
                    "%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%229177ba6f883473505dc99fcf2b679a6e270af6320a157f0798b92efeab98d5d3%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6dHJ1ZSwic2t1c0ZpbHRlciI6IkFMTCIsInNpbXVsYXRpb25CZWhhdmlvciI6ImRlZmF1bHQiLCJpbnN0YWxsbWVudENyaXRlcmlhIjoiTUFYX1dJVEhPVVRfSU5URVJFU1QiLCJwcm9kdWN0T3JpZ2luVnRleCI6ZmFsc2UsIm1hcCI6ImMsYyIsInF1ZXJ5IjoiZWxlY3Ryb2RvbWVzdGljb3MteS10ZWNub2xvZ2lhL2VsZWN0cm8taG9nYXIiLCJvcmRlckJ5IjoiT3JkZXJCeVNjb3JlREVTQyIsImZyb20iOjAsInRvIjoxMSwic2VsZWN0ZWRGYWNldHMiOlt7ImtleSI6ImMiLCJ2YWx1ZSI6ImVsZWN0cm9kb21lc3RpY29zLXktdGVjbm9sb2dpYSJ9LHsia2V5IjoiYyIsInZhbHVlIjoiZWxlY3Ryby1ob2dhciJ9XSwiZmFjZXRzQmVoYXZpb3IiOiJTdGF0aWMiLCJjYXRlZ29yeVRyZWVCZWhhdmlvciI6ImRlZmF1bHQiLCJ3aXRoRmFjZXRzIjpmYWxzZSwidmFyaWFudCI6IjY2ODQ0ZDg0MGU4OTA0MzBmODU3ZGVlZi12YXJpYW50TnVsbCIsImFkdmVydGlzZW1lbnRPcHRpb25zIjp7InNob3dTcG9uc29yZWQiOnRydWUsInNwb25zb3JlZENvdW50IjozLCJhZHZlcnRpc2VtZW50UGxhY2VtZW50IjoidG9wX3NlYXJjaCIsInJlcGVhdFNwb25zb3JlZFByb2R1Y3RzIjp0cnVlfX0%3D%22%7D"
                )
            )
        except Exception as e:
            print(f"Error al decodificar la URL inicial: {e}")
            raise

    def _fetch_page_data(self, url_decoded, start, page_size):
        try:
            variables = json.loads(base64_decode(url_decoded["variables"]))
            variables.update(
                {
                    "from": start,
                    "to": start + page_size,
                    "query": "electrodomesticos-y-tecnologia",
                }
            )
            url_decoded["variables"] = base64_encode(json.dumps(variables)).decode(
                "utf-8"
            )
            extension_fin = url_encode(json.dumps(url_decoded))
            productos_olimpica = self.olimpica_scraper.extrae_data(extension_fin)

            if not productos_olimpica:
                print(f"No se encontraron productos en la página con 'from': {start}")
                return pd.DataFrame()

            if not (
                isinstance(productos_olimpica, dict)
                and "data" in productos_olimpica
                and "productSearch" in productos_olimpica["data"]
            ):
                print(
                    f"Formato inesperado en la respuesta para la página con 'from': {start}"
                )
                return pd.DataFrame()

            productos = productos_olimpica["data"]["productSearch"]["products"]
            if not productos:
                print("No hay más productos disponibles.")
                return pd.DataFrame()

            return pd.DataFrame(
                [self.olimpica_adapter.adapt(product) for product in productos]
            )
        except Exception as e:
            print(f"Error al procesar la página con 'from': {start}, error: {e}")
            return pd.DataFrame()
