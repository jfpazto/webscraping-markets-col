from fastapi import FastAPI, HTTPException, Query
from service.falabella_service import FalabellaService
from service.mercados_disponibles import TiendasDisponibles
from service.exito_service import ExitoService
from service.homecenter_service import HomecenterService
from service.olimpica_service import OlimipicaService
from pathlib import Path
import pandas as pd
import sys
import os
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from processors.analyze_data import AnalyzeData
import json

sys.path.append(str(Path(__file__).resolve().parents[1]))


class MarketScrapingAPI:
    def __init__(self):
        self.app = FastAPI(
            title="Market Scraping",
            description="Scraping in different markets in Colombia",
            version="1.0.0",
        )
        # Configuración del middleware CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],  # URL del frontend
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.exito_service = ExitoService()
        self.homecenter_service = HomecenterService()
        self.falabella_service = FalabellaService()
        self.tiendas_disponibles = TiendasDisponibles()
        self.tienda_olimpica = OlimipicaService()

        self.add_routes()

    def add_routes(self):
        self.add_homecenter_routes()
        self.add_falabella_routes()
        self.add_mercados_routes()
        self.add_exito_routes()
        self.add_olimpica_routes()
        self.lista_snapshots()
        self.retorna_productos()

    def add_homecenter_routes(self):
        @self.app.get("/homecenter/categorias")
        def obtener_categorias():
            return self.homecenter_service.obtener_categorias()

        @self.app.get("/homecenter/productos")
        def obtener_productos():
            try:
                productos = self.homecenter_service.obtener_productos()
                productos.to_csv("homecenter.csv", index=False)
                return productos.to_dict(orient="records")
            except TypeError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener productos para tienda HomeCenter: {e}",
                )

    def add_falabella_routes(self):
        @self.app.get("/falabella/productos")
        def obtener_productos_falabella():
            try:
                productos_falabella = (
                    self.falabella_service.retorna_productos_falabella()
                )
                df = productos_falabella
                df.to_csv("falabella.csv", index=False)
                print("Productos Guardados")
                return df.to_dict(orient="records")
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error al obtener productos de Exito: {e}"
                )

    def add_mercados_routes(self):
        @self.app.get("/mercados")
        def obtener_mercados_disponibles():
            return self.tiendas_disponibles.retorna_mercados_disponibles()

    def add_exito_routes(self):
        @self.app.get("/exito/productos")
        def obtener_productos_exito():
            try:
                productos = self.exito_service.retorna_productos_exito()
                productos.to_csv("exito.csv", index=False)
                return productos.to_dict(orient="records")
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error al obtener productos de Exito: {e}"
                )

    def add_olimpica_routes(self):
        @self.app.get("/olimpica/products")
        def obtiene_prodcutos_olimpica():
            try:
                productos = self.tienda_olimpica.extrae_productos_olimpica()
                productos.to_csv("olimpica.csv", index=False)
                return productos.to_dict(orient="records")
            except TypeError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener productos para tienda olimpica: {e}",
                )

    def lista_snapshots(self):
        @self.app.get("/files/{tienda}", response_model=list[str])
        def listar_archivos(tienda: str):
            print("Buscando archivos en la tienda:", tienda)
            tienda_path = os.path.join("output", tienda)
            if not os.path.exists(tienda_path):
                raise HTTPException(status_code=404, detail="Tienda no encontrada")

            print(f"Contenido del directorio {tienda_path}: {os.listdir(tienda_path)}")
            archivos = tuple(os.listdir(tienda_path))
            print(f"Archivos encontrados: {archivos}")
            return archivos

    def retorna_productos(self):
        @self.app.get("/files/{tienda}/{snapshot}", response_model=dict)
        def retorna_productos_tienda(
            tienda: str,
            snapshot: str,
            page: int = Query(1, ge=1),  # Número de página (por defecto 1)
            limit: int = Query(
                10, ge=1
            ),  # Número máximo de elementos por página (por defecto 10)
        ):
            try:
                # Construye la ruta del archivo incluyendo el subdirectorio del snapshot
                filepath = os.path.join(
                    "output", tienda, snapshot, f"{tienda}_{snapshot}.csv"
                )
                print(f"Buscando archivo en: {filepath}")

                # Verifica si el archivo existe
                if not os.path.exists(filepath):
                    raise HTTPException(status_code=404, detail="Archivo no encontrado")

                # Lee el archivo CSV
                df = pd.read_csv(filepath)
                print(f"Archivo encontrado: {filepath}")

                # Reemplaza los valores NaN con una cadena vacía o un valor predeterminado
                df = df.fillna("")  # También puedes usar df.fillna(0) para números

                # Realiza el análisis de datos
                analysis = AnalyzeData.analyze_data(self, df)

                # Convierte el DataFrame a una lista de diccionarios
                data = df.to_dict(orient="records")

                # Total de registros
                total_records = len(data)

                # Calcula el offset basado en la página
                offset = (page - 1) * limit

                # Verifica si el offset está fuera de rango
                if offset >= total_records:
                    raise HTTPException(status_code=404, detail="Página fuera de rango")

                # Aplica el paginado
                paginated_data = data[offset : offset + limit]

                # Calcula la página actual
                current_page = page

                # Construye la respuesta con metadatos y análisis
                response = {
                    "total_records": total_records,
                    "current_page": current_page,
                    "limit": limit,
                    "offset": offset,
                    "data": paginated_data,
                    "analysis": analysis,
                }

                # Guarda la respuesta en un archivo JSON
                json_output_path = os.path.join(
                    "output", tienda, snapshot, f"{tienda}_{snapshot}_page{page}.json"
                )
                with open(json_output_path, "w", encoding="utf-8") as json_file:
                    json.dump(response, json_file, ensure_ascii=False, indent=4)
                print(f"Datos guardados en: {json_output_path}")

                # Devuelve la respuesta
                return response
            except Exception as e:
                print(f"Error al obtener productos tienda: {e}")
                raise HTTPException(
                    status_code=500, detail="Error interno del servidor"
                )


market_scraping_api = MarketScrapingAPI()

app = market_scraping_api.app
