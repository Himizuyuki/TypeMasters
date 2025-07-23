from sqlalchemy import Engine
from sqlalchemy import create_engine
import os

def create_engine_default() -> Engine:
    return create_engine(f"mysql+pymysql://:1234@typemasters-db-container/typemasters")
