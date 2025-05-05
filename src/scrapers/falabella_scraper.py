import requests
import urllib3
from urllib.parse import quote
from bs4 import BeautifulSoup
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FalabellaScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.paginator = 3

    def get_falabella_products(self, page):
        try:
            url = (
                f"https://www.falabella.com.co/s/browse/v1/listing/co"
                f"?page={page}&categoryId=cat50868&categoryName=Tecnologia&pgid=10&pid=bbea9a06-99b1-44de-bc6e-d314bca4fad3"
            )
            print("URL", url)
            response = requests.get(url, headers=self.headers, verify=False)  # nosec
            response.raise_for_status()
            return (response.json(), response.status_code)
        except Exception as e:
            print(f"Error al obtener productos de Falabella durante el scraping : {e}")
            return ""

    def get_falabella_products_electrohogar(self, page):
        try:
            url = (
                f"https://www.falabella.com.co/s/browse/v1/listing/co"
                f"?page={page}&categoryId=cat50623&categoryName=Tecnologia&pgid=10&pid=bbea9a06-99b1-44de-bc6e-d314bca4fad3"
            )
            print("URL", url)
            response = requests.get(url, headers=self.headers, verify=False)  # nosec
            response.raise_for_status()
            return (response.json(), response.status_code)
        except Exception as e:
            print(f"Error realizando scrping para categoria ElectroHogar: {e}")
            return ""

    def get_falabella_category_products(self, link_product):
        list_categories = []
        url = link_product
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, verify=False)  # nosec
        soup = BeautifulSoup(response.text, "html.parser")
        ld_json = soup.find("script", type="application/ld+json")
        if ld_json:
            try:
                data = json.loads(ld_json.string)
                if isinstance(data, dict) and "itemListElement" in data:
                    breadcrumb = data["itemListElement"]
                    if len(breadcrumb) > 2:
                        nombre_pos1 = breadcrumb[1]["item"]["name"]
                        nombre_pos2 = breadcrumb[2]["item"]["name"]
                        list_categories.append(nombre_pos1)
                        list_categories.append(nombre_pos2)
                        return list_categories
                    else:
                        nombre_pos1 = breadcrumb[1]["item"]["name"]
                        nombre_pos2 = breadcrumb[1]["item"]["name"]
                        list_categories.append(nombre_pos1)
                        list_categories.append(nombre_pos2)
                        return list_categories
                else:
                    print("No se encontró itemListElement en el JSON.")
                    return list_categories
            except Exception:
                print(link_product)
                return list_categories
        else:
            print("No se encontró la etiqueta <script type='application/ld+json'>")
            return list_categories
