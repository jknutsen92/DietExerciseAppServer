import platform

from databases  import Database
from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine
from backup     import load_db_from_cloud, load_db_from_external_cache, write_db_to_external_cache
from cfg        import *

# TODO abstract this into a backup class
"""
if EXTERNAL_DB_CACHING:
    system = platform.system()
    if system == "Linux":
        load_db_from_external_cache(LOCAL_DB_PATH_LINUX, EXTERNAL_DB_PATH_LINUX, DATABASE_NAME)
    elif system == "Windows":
        load_db_from_external_cache(LOCAL_DB_PATH_WINDOWS, EXTERNAL_DB_PATH_WINDOWS, DATABASE_NAME)
if CLOUD_DB_CACHING:
    load_db_from_cloud()
"""

# DB Init
metadata = MetaData()
db = Database(DATABASE_URL)

# Table Init
items = Table(
    "items",
    metadata,
    Column("id",            Integer,        primary_key=True),
    Column("name",          String(50)),
    Column("description",   String(1000),   nullable=True),
    Column("owner_id",      Integer)
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
metadata.create_all(engine)

# DB cleanup
# TODO: abstract this into a backup class
"""
def cleanup_databases():
    if EXTERNAL_DB_CACHING:
        system = platform.system()
        if system == "Linux":
            write_db_to_external_cache(LOCAL_DB_PATH_LINUX, EXTERNAL_DB_PATH_LINUX, DATABASE_NAME)
        elif system == "Windows":
            write_db_to_external_cache(LOCAL_DB_PATH_WINDOWS, EXTERNAL_DB_PATH_WINDOWS, DATABASE_NAME)
    elif CLOUD_DB_CACHING:
        pass
"""