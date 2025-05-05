from adapters.base_adapter import BaseAdapter
from dto.producto_dto import ProductoDTO
from datetime import date
from scrapers.falabella_scraper import FalabellaScraper
import logging


class FalabellaAdapter(BaseAdapter):
    def parse_raw_data(
        self, raw_data, exchange_rate, store_url, currency
    ) -> ProductoDTO:
        try:
            sku = raw_data["skuId"]
            title = raw_data["displayName"]
            available = raw_data.get("availability", False)
            lista_regular = self.extrae_precios(raw_data["prices"], 1)
            price_regular = lista_regular[0] if len(lista_regular) > 0 else 0
            lista_oferta = self.extrae_precios(raw_data["prices"], 2)
            price_offer = lista_oferta[0] if len(lista_oferta) > 0 else price_regular
            price_offer_allies = self.extrae_precios(raw_data["prices"], 3)
            price_other_sellers = self.extrae_precios(raw_data["prices"], 3)  # todo
            price_regular_usd = int(price_regular / exchange_rate)
            price_offer_usd = int(price_offer / exchange_rate)
            discount = price_offer - price_regular
            product_img_urls = raw_data["mediaUrls"][0]
            brand = raw_data["brand"] if "brand" in raw_data else "Sin Marca"
            url = raw_data["url"]
            product_group = "Tecnologia"
            product_subgroup = "Tecnologia"
            dt = date.today()
            producto = ProductoDTO(
                sku,
                title,
                available,
                price_regular,
                price_offer,
                price_offer_allies,
                price_other_sellers,
                price_regular_usd,
                price_offer_usd,
                discount,
                currency,
                product_img_urls,
                brand,
                product_group,
                product_subgroup,
                url,
                store_url,
                dt,
            )

            return producto.to_dict()
        except Exception as e:
            print(f"Error al mapear producto de Éxito: {e}, SKU:", sku)
            return None

    def adapt(self, raw_data):
        return self.parse_raw_data(
            raw_data=raw_data,
            exchange_rate=5000,
            store_url="https://www.falabella.com",
            currency="COP",
        )

    def extrae_precios(self, lista_precios, type):
        txt = ["normalPrice"]
        text = ["eventPrice", "internetPrice"]
        precios = []
        if type == 1:
            for precio in lista_precios:
                if precio["type"] in txt and len(lista_precios) > 0:
                    precios.append(int(precio["price"][0].replace(".", "")))
        elif type == 2:
            for precio in lista_precios:
                if precio["type"] in text and len(lista_precios) > 0:
                    precios.append((int(precio["price"][0].replace(".", ""))))
        elif type == 3:
            for precio in lista_precios:
                if (
                    precio["type"] not in text
                    and precio["type"] not in txt
                    and len(lista_precios) > 0
                ):
                    precios.append(
                        (precio["type"], int(precio["price"][0].replace(".", "")))
                    )
        return precios

    def get_category_product(self, link):
        category_list = FalabellaScraper.get_falabella_category_products(self, link)
        return category_list
