import pandas as pd
import json
from scrapers.homecenter_scraper import HomecenterScrapper
from adapters.homecenter_adapter import HomeCenterAdapter
from utils import io_utils


class HomecenterProcessor:
    def __init__(self):
        self.categorias_path = "src/data/homecenter_categorias.json"
        self.scraper_homecenter = HomecenterScrapper()
        self.adapter_homecenter = HomeCenterAdapter()

    def procesa_productos(self):
        df_total = None
        productos_homecenter = []
        for page in range(1, 171):
            productos = self.scraper_homecenter.get_homecenter_products(page)["data"][
                "results"
            ]
            productos_homecenter.extend(productos)
        list_productos = []
        for producto in productos_homecenter:
            list_productos.append(self.adapter_homecenter.adapt(producto))
            if df_total is None:
                df_total = pd.DataFrame([self.adapter_homecenter.adapt(producto)])
            else:
                df_total = pd.concat(
                    [df_total, pd.DataFrame([self.adapter_homecenter.adapt(producto)])],
                    ignore_index=True,
                )
        return df_total
