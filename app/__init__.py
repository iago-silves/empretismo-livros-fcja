from app.infra.database import engine, metadata
from app.infra.mappers.mapper import start_mappers

def create_app():
    start_mappers()
    metadata.create_all(engine)
