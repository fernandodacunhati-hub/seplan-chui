import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from database import Base, engine

load_dotenv()

print(f"Tentando conectar com: {os.getenv('DATABASE_URL')}")

try:
    # Força a criação das tabelas
    Base.metadata.create_all(bind=engine)
    print("SUCCESS: Tabelas criadas com sucesso no Supabase!")
except Exception as e:
    print("\nERRO DE CONEXAO:")
    print(e)
