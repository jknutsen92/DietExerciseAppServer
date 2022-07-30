from cfg                    import *
from pathlib                import Path
from Google                 import Create_Service
from googleapiclient.http   import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
from shutil                 import copyfile
from datetime               import datetime
from io                     import BytesIO

def load_db_from_external_cache(local_path: str, external_path:str, db_name:str) -> None:
    local = Path(f"{local_path}{db_name}")
    extern = Path(f"{external_path}{db_name}")

    if not local.exists():
        local.parent.mkdir()
        local.touch()

    if extern.exists():
        if not local.exists() or local.stat().st_mtime < extern.stat().st_mtime:
            copyfile(extern, local)
        

def load_db_from_cloud(local_path, db_name):
    local = Path(f"{local_path}{db_name}")
    service = Create_Service(G_CLIENT_SECRET_FILE, G_API_NAME, G_API_VERSION, G_SCOPES)

    try:
        response = service.files().list(q="name='databases'", fields="files(id)").execute()
        folder_id = response.get("files")[0]["id"]

        query = f"name='{DATABASE_NAME}' and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="files(id, modifiedTime)").execute()
        file = response.get("files")[0]

        cloud_dt = datetime.strptime(file["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if cloud_dt.timestamp() > local.stat().st_mtime:
            request = service.files().get_media(fileId=file["id"])
            backup_file = BytesIO()
            downloader = MediaIoBaseDownload(backup_file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"{DATABASE_NAME} download {int(status.progress() * 100)}% completed")

            with open(local, "wb") as localFile:
                localFile.write(backup_file.getbuffer())

    except HttpError as e:
        print(f"Could not find {DATABASE_NAME} in drive")
        print(e)
    

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

    folder_meta = {
        "name":     "databases",
        "mimeType": "application/vnd.google-apps.folder"
    }
    try:
        response = service.files().list(q="name = 'databases'", fields="files(id)").execute()
        folder_id = response.get("files")[0]["id"]
    except HttpError as e:
        print(e)
        response = service.files().create(body=folder_meta, fields="id").execute()
        folder_id = response.get("id")


    file_metadata = { "name": f"{db_name}", "parents": [folder_id] }
    media = MediaFileUpload(local)
    
    query = f"name='{db_name}' and '{folder_id}' in parents"
    response = service.files().list(q=query, fields="files(id)").execute()
    files = response.get("files")
    if files:
        service.files().update(body=file_metadata, media_body=media, fileId=files[0]["id"])
    else:
        service.files().create(body=file_metadata, media_body=media).execute()
    


#load_db_from_cloud("databases/", "store.db")
#write_db_to_cloud("databases/", "store.db")