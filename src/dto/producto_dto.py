from datetime import date


class ProductoDTO:
    def __init__(
        self,
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
        store,
        dt,
    ):
        self.sku = sku
        self.title = title
        self.available = available
        self.price_regular = price_regular
        self.price_offer = price_offer
        self.price_offer_allies = price_offer_allies
        self.price_other_sellers = price_other_sellers
        self.price_regular_usd = price_regular_usd
        self.price_offer_usd = price_offer_usd
        self.discount = discount
        self.currency = currency
        self.product_img_urls = product_img_urls
        self.brand = brand
        self.product_group = product_group
        self.product_subgroup = product_subgroup
        self.url = url
        self.store = store
        self.dt = dt

    def to_dict(self):
        return {
            "PRODUCT GROUP": self.product_group,
            "PRODUCT SUBGROUP": self.product_subgroup,
            "BRAND": self.brand,
            "SKU": self.sku,
            "TITLE": self.title,
            "URL": self.url,
            "PRODUCT IMG URL": self.product_img_urls,
            "AVAILABLE": self.available,
            "CURRENCY": self.currency,
            "PRICE REGULAR": self.price_regular,
            "PRICE OFFER": self.price_offer,
            "PRICE REGULAR USD": self.price_regular_usd,
            "PRICE OFFER USD": self.price_offer_usd,
            "PRICE OFFER ALLIES": self.price_offer_allies,
            "PRICE OTHER SELLERS": self.price_other_sellers,
            "DISCOUNT": self.discount,
            "DISCOUNT PCT": "NO",
            "STORE": self.store,
            "DT": self.dt.isoformat() if isinstance(self.dt, date) else self.dt,
        }
