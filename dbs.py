from databases  import Database
from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine
from backup     import Backup

DATABASE_NAME               = "store.db"
BACKUP_CONFIG_FILE          = "config/backup.json"
DATABASE_URL                = f"sqlite:///databases/{DATABASE_NAME}"

database_backup = Backup(
                    DATABASE_NAME, 
                    BACKUP_CONFIG_FILE,
                    external_drive_caching=True,
                    cloud_caching=True
)
database_backup.load()

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