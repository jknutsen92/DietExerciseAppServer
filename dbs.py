from databases  import Database
from sqlalchemy import MetaData, Table, Column, Integer, String
from funcs      import load_db_from_external_cache, write_db_to_external_cache

import platform


EXTERNAL_DB_CACHING             = True
CLOUD_DB_CACHING                = False
EXTERNAL_DB_PATH_WINDOWS        = "F:\\databases\\"
EXTERNAL_DB_PATH_LINUX          = "/run/media/jeffrey/DATA/databases/"
LOCAL_DB_PATH_WINDOWS           = "databases\\"
LOCAL_DB_PATH_LINUX             = "databases/"
DATABASE_NAME                   = "store.db"
DATABASE_URL                    = f"sqlite:///databases/{DATABASE_NAME}"


if EXTERNAL_DB_CACHING:
    system = platform.system()
    if system == "Linux":
        load_db_from_external_cache(LOCAL_DB_PATH_LINUX, EXTERNAL_DB_PATH_LINUX, DATABASE_NAME)
    elif system == "Windows":
        load_db_from_external_cache(LOCAL_DB_PATH_WINDOWS, EXTERNAL_DB_PATH_WINDOWS, DATABASE_NAME)
elif CLOUD_DB_CACHING:
    # TODO
    pass


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

# DB cleanup
def cleanup_databases():
    if EXTERNAL_DB_CACHING:
        system = platform.system()
        if system == "Linux":
            write_db_to_external_cache(LOCAL_DB_PATH_LINUX, EXTERNAL_DB_PATH_LINUX, DATABASE_NAME)
        elif system == "Windows":
            write_db_to_external_cache(LOCAL_DB_PATH_WINDOWS, EXTERNAL_DB_PATH_WINDOWS, DATABASE_NAME)
    elif CLOUD_DB_CACHING:
        pass
