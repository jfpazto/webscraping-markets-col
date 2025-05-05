from datetime import date
from adapters.base_adapter import BaseAdapter
from dto.producto_dto import ProductoDTO
from scrapers.exito_scraper import ExitoScraper


class OlimpicaAdapter(BaseAdapter):
    def parse_raw_data(
        self, raw_data, exchange_rate, store_url, currency
    ) -> ProductoDTO:
        try:
            sku = raw_data["productId"]
            title = raw_data["productName"]
            available = True  # raw_data['sellers'][0]['commertialOffer']['AvailableQuantity'] #todo
            price_regular = raw_data["priceRange"]["listPrice"]["highPrice"]
            price_offer = raw_data["priceRange"]["sellingPrice"]["highPrice"]
            price_offer_allies = ""
            price_other_sellers = ""
            price_regular_usd = int(price_regular / exchange_rate)
            price_offer_usd = int(price_offer / exchange_rate)
            discount = price_offer - price_regular
            product_img_urls = raw_data["items"][0]["images"][0]["imageUrl"]
            brand = raw_data["brand"]
            product_group = raw_data["categories"][2].split("/")[1]
            product_subgroup = raw_data["categories"][1].split("/")[2]
            url = store_url + raw_data["link"]
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
        except TypeError as e:
            print(f"Error al mapear producto de Olimpica: {e}")
            return None

    def adapt(self, raw_data):
        return self.parse_raw_data(
            raw_data=raw_data,
            exchange_rate=5000,
            store_url="https://www.olimpica.com",
            currency="COP",
        )
