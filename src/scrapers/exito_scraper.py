import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ExitoScraper:
    def __init__(self):
        self.base_url = "https://www.exito.com/api/graphql"
        self.headers = {
            "Host": "www.exito.com",
            "Cookie": "janus_sid=c71590ad-20ca-4ec4-8354-4f3e27455de7",
            "Content-Type": "application/json",
        }

    def get_exito_products(self, page):
        url = f"{self.base_url}?operationName=QuerySearch"
        payload = json.dumps(
            {
                "operationName": "QuerySearch",
                "variables": {
                    "first": 50,
                    "after": str(page),
                    "sort": "score_desc",
                    "term": "",
                    "selectedFacets": [
                        {"key": "category-1", "value": "tecnologia"},
                        {
                            "key": "channel",
                            "value": '{"salesChannel":"1","regionId":""}',
                        },
                        {"key": "locale", "value": "es-CO"},
                    ],
                },
            }
        )

        try:
            response = requests.request(
                "POST", url, headers=self.headers, data=payload, verify=False  # nosec
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener productos de Éxito: {e}")
            return None

    def valida_producto_sku(self, sku_id):
        url = f"{self.base_url}?operationName=GetProductsBySkuIds"
        payload = json.dumps(
            {
                "operationName": "GetProductsBySkuIds",
                "variables": {"skuIds": [str(sku_id)], "vtexSegment": ""},
            }
        )

        try:
            response = requests.request(
                "POST", url, headers=self.headers, data=payload, verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al validar el SKU del producto: {e}")
            return None
