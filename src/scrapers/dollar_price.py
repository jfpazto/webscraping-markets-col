import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DollarPriceScraper:
    def __init__(self):
        self.url = "https://www.dolar-colombia.com/"
        self.headers = {}

    def get_dollar_price(self):
        try:
            response = requests.request(
                "GET", self.url, headers=self.headers, verify=False  # nosec
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            exchange_rate_element = soup.find("span", class_="exchange-rate")
            if exchange_rate_element:
                exchange_rate = exchange_rate_element.text.strip().replace(",", "")
                return float(exchange_rate)
            else:
                print("No se encontró el valor de la tasa de cambio.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener el precio del dólar: {e}")
            return None
