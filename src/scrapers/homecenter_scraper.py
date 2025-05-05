import requests
import urllib3
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HomecenterScrapper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_homecenter_products(self, page):
        try:
            headers = self.headers
            url = f"https://www.homecenter.com.co/s/search/v1/soco/category/products?&priceGroup=10&zone=1&currentpage={page}&channel=kiosk&categoryId=cat10374"
            response = requests.get(url, headers=headers, verify=False)  # nosec
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al obtener productos de Homecenter: {e}")
            return None
