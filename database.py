import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém a URL do banco do arquivo .env
POSTGRES_URL = os.getenv("DATABASE_URL")

if not POSTGRES_URL:
    raise RuntimeError("A variável DATABASE_URL não foi configurada no arquivo .env!")

# Compatibilidade do prefixo para SQLAlchemy
if POSTGRES_URL.startswith("postgres://"):
    POSTGRES_URL = POSTGRES_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(POSTGRES_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# TABELA 1: Licenciamento de Obras
class AnaliseObraDB(Base):
    __tablename__ = "analises_obras"

    id = Column(Integer, primary_key=True, index=True)
    data_analise = Column(DateTime, default=datetime.now)
    zona = Column(String(50))
    area_lote_m2 = Column(Float)
    area_construida_terreo_m2 = Column(Float)
    area_construida_total_m2 = Column(Float)
    recuo_frontal_m = Column(Float)
    aprovado = Column(Boolean)
    taxa_ocupacao_calculada = Column(Float)
    indice_aproveitamento_calculado = Column(Float)
    parecer_tecnico = Column(Text)

# TABELA 2: Propostas de Captação
class PropostaRecursoDB(Base):
    __tablename__ = "propostas_recursos"

    id = Column(Integer, primary_key=True, index=True)
    edital_id = Column(String(100))
    fonte = Column(String(100))
    orgao = Column(String(200))
    programa = Column(Text)
    valor_disponivel_brl = Column(Float)
    status_proposta = Column(String(50), default="Em Elaboração")
    data_registro = Column(DateTime, default=datetime.now)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
