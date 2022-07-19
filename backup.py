from cfg                    import *
from pathlib                import Path
from Google                 import Create_Service
from googleapiclient.http   import MediaFileUpload
from googleapiclient.errors import HttpError
from shutil                 import copyfile

def load_db_from_external_cache(local_path: str, external_path:str, db_name:str) -> None:
    local = Path(f"{local_path}{db_name}")
    extern = Path(f"{external_path}{db_name}")

    if not local.exists():
        local.parent.mkdir()
        local.touch()

    if extern.exists():
        if not local.exists() or local.stat().st_mtime < extern.stat().st_mtime:
            copyfile(extern, local)
        

def load_db_from_cloud():
    service = Create_Service(G_CLIENT_SECRET_FILE, G_API_NAME, G_API_VERSION, G_SCOPES)

    response = service.files().list(q={
        "name":     f"{G_DRIVE_FOLDER}/{DATABASE_NAME}"         
    }).execute()

    print(response)
    

def write_db_to_external_cache(local_path: str, external_path: str, db_name: str) -> None:
    local = Path(f"{local_path}{db_name}")
    extern = Path(f"{external_path}{db_name}")

    if not extern.parent.exists():
        try:
            extern.parent.mkdir()
        except IOError:
            raise IOError(f"Could not access external storage device at {extern}")

    copyfile(local, extern)
    Path(f"{local_path}{db_name}").touch()

def write_db_to_cloud(local_path, db_name):
    local = Path(f"{local_path}{db_name}")
    service = Create_Service(G_CLIENT_SECRET_FILE, G_API_NAME, G_API_VERSION, G_SCOPES)

    file_metadata = { "name": f"{db_name}", "folder": G_DRIVE_FOLDER }
    media = MediaFileUpload(local)

    service.files().create(body=file_metadata, media_body=media).execute()


#load_db_from_cloud()
write_db_to_cloud("databases/", "store.db")