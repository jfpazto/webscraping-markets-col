from datetime import date
from adapters.base_adapter import BaseAdapter
from dto.producto_dto import ProductoDTO
from scrapers.exito_scraper import ExitoScraper


class ExitoAdapter(BaseAdapter):
    def parse_raw_data(
        self, raw_data, exchange_rate, store_url, currency
    ) -> ProductoDTO:
        try:
            sku = raw_data["node"]["sku"]
            title = raw_data["node"]["name"]
            available = self.valida_disponibilidad_producto(sku, "exito") >= 0
            price_regular = raw_data["node"]["sellers"][0]["commertialOffer"][
                "PriceWithoutDiscount"
            ]
            price_offer = raw_data["node"]["sellers"][0]["commertialOffer"]["Price"]
            price_offer_allies = self.procesa_precios_oferta(
                raw_data["node"]["sellers"][0]["commertialOffer"]["teasers"],
                price_regular,
            )
            price_other_sellers = self.procesa_otros_vendedores(
                raw_data["node"]["sellers"], sku
            )
            price_regular_usd = int(price_regular / exchange_rate)
            price_offer_usd = int(price_offer / exchange_rate)
            discount = price_offer - price_regular
            product_img_urls = raw_data["node"]["image"][0]["url"]
            brand = raw_data["node"]["brand"]["name"]
            product_group = raw_data["node"]["breadcrumbList"]["itemListElement"][0][
                "name"
            ]
            product_subgroup = raw_data["node"]["breadcrumbList"]["itemListElement"][2][
                "name"
            ]
            url = self.retorna_url_producto(
                raw_data["node"]["breadcrumbList"]["itemListElement"], store_url
            )
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
            store_url="https://www.exito.com",
            currency="COP",
        )

    def procesa_otros_vendedores(self, vendedores, sku):
        productos_exito = []
        for vendedor in vendedores:
            try:
                name_seller = vendedor["sellerName"]
                if name_seller.lower() != "exito":
                    precio_producto = vendedor["commertialOffer"]["Price"]
                    cantidad_disponible = self.valida_disponibilidad_producto(
                        sku, name_seller
                    )
                    productos_exito.append(
                        (name_seller, precio_producto, cantidad_disponible)
                    )
            except Exception as e:
                print(f"Error al procesar el vendedor: {e}")
        return productos_exito

    def procesa_precios_oferta(self, lista_aliados, precio_real):
        lista_precios_aliados = []
        for aliado in lista_aliados:
            try:
                name_aliado = aliado["name"]
                precio_producto = int(
                    float(aliado["effects"]["parameters"][1]["value"])
                )
                precio_final = precio_real - precio_producto
                lista_precios_aliados.append((name_aliado, precio_final))
            except Exception as e:
                print(f"Error al procesar el aliado: {e}")
        return lista_precios_aliados

    def retorna_categoria_producto(self, list_categorias, nivel):
        try:
            return list_categorias[nivel - 1]["name"].upper()
        except IndexError:
            print(f"Nivel {nivel} no válido en las categorías")
            return None
        except Exception as e:
            print(f"Error al obtener categorías de productos: {e}")
            return None

    def retorna_url_producto(self, list_categorias, url_store):
        try:
            path = list_categorias[len(list_categorias) - 1]["item"]
            return f"{url_store}{path}"
        except Exception as e:
            print(f"Error al obtener la URL del producto: {e}")
            return None

    def valida_disponibilidad_producto(self, sku_id, name_aliado):
        try:
            scraper_exito = ExitoScraper()
            producto = scraper_exito.valida_producto_sku(sku_id)
            for seller in producto["data"]["getProductsBySkuIds"][0]["items"][0][
                "sellers"
            ]:
                if seller["sellerName"] == name_aliado:
                    return seller["commertialOffer"]["AvailableQuantity"]
            return None
        except Exception as e:
            print(f"Error al validar la disponibilidad del producto: {e}")
            return False
