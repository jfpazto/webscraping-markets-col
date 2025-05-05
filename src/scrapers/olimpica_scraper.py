import requests
import json
import urllib3
from utils.io_utils import url_encode, url_decode

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OlimpicaScraper:
    def __init__(self):
        self.payload = {}
        self.headers = {"Content-Type": "application/json"}

    def extrae_data(self, extension):
        try:
            url = f"https://www.olimpica.com/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-CO&__bindingId=6e864c25-6c9e-4bf6-84e0-a4c1f4d151e4&operationName=productSearchV3&variables=%7B%7D&extensions={extension}"
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                data=self.payload,
                verify=False,  # nosec
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al obtener productos de Olímpica: {e}")
            return None
