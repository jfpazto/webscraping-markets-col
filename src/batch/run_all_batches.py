import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from batch.run_falabella import FalabellaBatch
from batch.run_exito import ExitoBatch
from batch.run_homecenter import HomeCenterBatch
from batch.run_olimpica import OlimpicaBatch
from pathlib import Path


class BatchRunner:
    def __init__(self):
        self.batches = [
            FalabellaBatch(),
            ExitoBatch(),
            HomeCenterBatch(),
            OlimpicaBatch(),
        ]

    def run_all_batches(self):
        print("Iniciando proceso de ejecución de todos los batches...")
        for batch in self.batches:
            try:
                batch.run()
            except Exception as e:
                print(f"Error al ejecutar el batch {batch.tienda}: {str(e)}")
        print("Proceso de ejecución de todos los batches finalizado.")


if __name__ == "__main__":
    batch_runner = BatchRunner()
    batch_runner.run_all_batches()
