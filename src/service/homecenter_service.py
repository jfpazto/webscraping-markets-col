from scrapers.homecenter_categories_scrapper import HomecenterCategoriesScraper
from scrapers.homecenter_scraper import HomecenterScrapper
from processors.homecenter_processors import HomecenterProcessor
from utils.io_utils import save_json
import pandas as pd


class HomecenterService:
    def __init__(self):
        self.scraper_category_homecenter = HomecenterCategoriesScraper()
        self.homecenter_processor = HomecenterProcessor()
        self.scraper_homecenter_products = HomecenterScrapper()

    def obtener_categorias(self):
        try:
            categorias = self.scraper_category_homecenter.get_categories()
            df_categorias = pd.DataFrame(
                {"id": range(1, len(categorias) + 1), "nombre": categorias}
            )
            categorias_json = df_categorias.to_dict(orient="records")
            save_json(categorias_json, "src/data/homecenter_categorias.json")
            print("Categorias Homecenter procesadas")
            return categorias_json
        except Exception as e:
            print(f"Error al obtener categorías de Homecenter: {e}")
            return None

    def obtener_productos(self):
        try:
            productos = self.homecenter_processor.procesa_productos()
            return productos
        except Exception as e:
            print(f"Error al obtener productos de Homecenter: {e}")
            return None
