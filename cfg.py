# Local database caching
EXTERNAL_DB_CACHING             = True
EXTERNAL_DB_PATH_WINDOWS        = "F:\\databases\\"
EXTERNAL_DB_PATH_LINUX          = "/run/media/jeffrey/DATA/databases/"
LOCAL_DB_PATH_WINDOWS           = "databases\\"
LOCAL_DB_PATH_LINUX             = "databases/"
DATABASE_NAME                   = "store.db"
DATABASE_URL                    = f"sqlite:///databases/{DATABASE_NAME}"
# Cloud database caching
CLOUD_DB_CACHING                = False
G_DRIVE_FOLDER                  = "databases"                   
G_CLIENT_SECRET_FILE            = "keys/client_secret.json"
G_API_NAME                      = "drive"
G_API_VERSION                   = "v3"
G_SCOPES                        = ["https://www.googleapis.com/auth/drive"]