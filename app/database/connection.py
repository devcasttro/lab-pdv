import sqlite3
import os

# Caminho absoluto com base na estrutura do projeto
DB_NAME = "labpdv.db"
DB_PATH = os.path.join(os.path.dirname(__file__), "..", DB_NAME)

def conectar():
    return sqlite3.connect(DB_PATH)
