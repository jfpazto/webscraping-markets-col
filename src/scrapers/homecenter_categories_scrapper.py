import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings(InsecureRequestWarning)


class HomecenterCategoriesScraper:
    def __init__(self):
        self.url = "https://www.homecenter.com.co/homecenter-co/"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
        }

    def get_categories(self):
        try:
            response = requests.get(
                self.url, headers=self.headers, verify=False  # nosec
            )  # nosec
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            category_name = []

            items = soup.find_all(
                "div",
                class_="list-item-menu-mobile ListItem-module__list-item___2BX8a ListItem-module__level-1___NNgf5",
            )
            for item in items:
                span = item.find("span")
                category_name.append(span.text.strip() if span else "Sin nombre")

            print("Categorías obtenidas:", category_name)
            return category_name
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener las categorías de Homecenter: {e}")
            return None
