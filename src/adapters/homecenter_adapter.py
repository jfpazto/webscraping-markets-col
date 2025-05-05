from adapters.base_adapter import BaseAdapter
from dto.producto_dto import ProductoDTO
from datetime import date


class HomeCenterAdapter(BaseAdapter):
    def parse_raw_data(
        self, raw_data, exchange_rate, store_url, currency
    ) -> ProductoDTO:
        try:
            sku = raw_data["skuId"]
            title = raw_data["displayName"]
            available = True  # Todo
            price_regular = (
                int(float(raw_data["prices"][1]["price"].replace(".", "")))
                if len(raw_data["prices"]) > 1
                else float(raw_data["prices"][0]["price"].replace(".", ""))
            )
            price_offer = float(raw_data["prices"][0]["price"].replace(".", ""))
            price_offer_allies = []
            price_other_sellers = []
            price_regular_usd = int(int(price_regular) / exchange_rate)
            price_offer_usd = int(int(price_offer) / exchange_rate)
            discount = price_offer - price_regular
            product_img_urls = raw_data["mediaUrls"][0]
            brand = raw_data["brand"]
            product_group = "TECNOLOGIA"  # Todo
            product_subgroup = "ELECTROHOGAR"  # Todo
            url = "https://www.homecenter.com.co/homecenter-co/product/" + str(sku)
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
            print(f"Error al mapear producto de Éxito: {e}")
            return None

    def adapt(self, raw_data):
        return self.parse_raw_data(
            raw_data=raw_data,
            exchange_rate=5000,
            store_url="https://www.homecenter.com",
            currency="COP",
        )
