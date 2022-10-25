from databases  import Database
from backup     import Backup
from sqlalchemy import (
    BigInteger,
    Column,
    create_engine,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    MetaData, 
    String,
    Table
)

DATABASE_NAME               = "dietapp.db"
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

class GenderEnum(Enum):
    male = 0
    female = 1

# Table Init
User = Table(
    "User",
    metadata,
    Column("id",                BigInteger,         primary_key=True),
    Column("email",             String(100),        nullable=False),
    Column("pass_hash",         String(64),         nullable=False),        # SHA-256
    Column("goal_id",           Integer,            nullable=True),
    Column("birthdate",         Date,               nullable=False),
    Column("weight",            Float,              nullable=False),
    Column("height",            Float,              nullable=False),
    Column("gender",            Enum(GenderEnum),   nullable=False)
)

Food = Table(
    "Food",
    metadata,
    Column("id",                String(40),         primary_key=True),      # SHA-1
    Column("name",              String(75),         nullable=False),
    Column("calories",          Float,              nullable=False),        # (kcal)
    Column("total_fat",         Float,              nullable=False),        # (g)
    Column("saturated_fat",     Float,              nullable=False),        # (g)
    Column("cholesterol",       Float,              nullable=False),        # (mg)
    Column("sodium",            Float,              nullable=False),        # (mg)
    Column("carbohydrates",     Float,              nullable=False),        # (g)
    Column("dietary_fiber",     Float,              nullable=False),        # (g)
    Column("sugars",            Float,              nullable=False),        # (g)
    Column("protein",           Float,              nullable=False),        # (g)
    Column("serving_qty",       Integer,            nullable=False),
    Column("serving_unit",      String(50),         nullable=False),
    Column("serving_weight",    Float,              nullable=False),        # (g)
    Column("image_url",         String(2048),       nullable=True)
)

FoodEaten = Table(
    "FoodEaten",
    metadata,
    Column("user_id",           BigInteger,         ForeignKey("User.id"), primary_key=True),
    Column("food_id",           String(40),         ForeignKey("Food.id"), primary_key=True),
    Column("time_consumed",     DateTime,           primary_key=True),
    Column("servings",          Float,              nullable=False)
)

Exercise = Table(
    "Exercise",
    metadata,
    Column("id",                String(40),         primary_key=True),      # SHA-1
    Column("name",              String(50),         nullable=False),
    Column("calories_per_hour", Float,              nullable=False)
)

ExerciseCompleted = Table(
    "ExerciseCompleted",
    metadata,
    Column("user_id",           BigInteger,         ForeignKey("User.id"), primary_key=True),
    Column("exercise_id",       String(40),         ForeignKey("Exercise.id"), primary_key=True),
    Column("time_completed",    DateTime,           primary_key=True),
    Column("duration",          Float,              nullable=True)
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
metadata.create_all(engine)