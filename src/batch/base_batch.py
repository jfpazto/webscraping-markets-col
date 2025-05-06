from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd
import boto3
import io
import requests


class BaseBatch(ABC):
    def __init__(self, tienda: str):
        self.tienda = tienda
        self.today = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.bucket_name = "mi-bucket-scraping-fabian"
        self.s3_prefix = f"{self.tienda}/{self.today}"

    @abstractmethod
    def run_service(self) -> pd.DataFrame:
        pass

    def check_ecs_credentials(self):
        print("🧪 Verificando acceso a metadata de ECS (http://169.254.170.2)...")
        try:
            r = requests.get("http://169.254.170.2/v2/credentials", timeout=2)
            print("✅ ECS metadata accesible. Código:", r.status_code)
            data = r.json()
            print("🔐 AccessKeyId:", data.get("AccessKeyId", "no visible"))
        except Exception as e:
            print("❌ No se pudo acceder a ECS metadata:", e)

    def save_to_s3(self, df: pd.DataFrame):
        self.check_ecs_credentials()

        try:
            filename = f"{self.tienda}_{self.today}.csv"
            s3_key = f"{self.s3_prefix}/{filename}"

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)

            s3 = boto3.client("s3")
            s3.put_object(Bucket=self.bucket_name, Key=s3_key, Body=csv_buffer.getvalue())

            print(f"✅ Archivo subido a S3: s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"❌ Error al subir el archivo a S3: {e}")

    def run(self):
        df = self.run_service()
        self.save_to_s3(df)
