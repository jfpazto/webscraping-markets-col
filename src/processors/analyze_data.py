import pandas as pd


class AnalyzeData:
    def analyze_data(self, df: pd.DataFrame) -> dict:
        try:
            # Categoría con más productos
            categoria_mas_productos = df["BRAND"].value_counts().idxmax()
            total_mas_productos = int(df["BRAND"].value_counts().max())

            # Categoría con menos productos
            categoria_menos_productos = df["BRAND"].value_counts().idxmin()
            total_menos_productos = int(df["BRAND"].value_counts().min())

            # Total de productos
            total_productos = int(len(df))

            # Productos disponibles
            productos_disponibles = int(df[df["AVAILABLE"]].shape[0])

            return {
                "categoria_mas_productos": {
                    "nombre": categoria_mas_productos,
                    "total": total_mas_productos,
                },
                "categoria_menos_productos": {
                    "nombre": categoria_menos_productos,
                    "total": total_menos_productos,
                },
                "total_productos": total_productos,
                "Total_disponibles": productos_disponibles,
            }
        except KeyError as e:
            raise ValueError(f"Falta una columna necesaria en el DataFrame: {e}")
