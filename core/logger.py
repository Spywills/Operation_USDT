# core/logger.py

import csv
from datetime import datetime
import os

def registrar_trade(tipo, preco, lucro=None, preco_entrada=None):
    path = "storage/trades.csv"
    novo_arquivo = not os.path.exists(path)

    with open(path, mode="a", newline="") as arquivo:
        writer = csv.writer(arquivo)

        if novo_arquivo:
            writer.writerow(["timestamp", "tipo", "preco", "lucro", "preco_entrada"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, tipo, preco, lucro, preco_entrada])
