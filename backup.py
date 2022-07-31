import platform
import pickle
import json

from pathlib                        import Path
from googleapiclient.http           import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors         import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow      import InstalledAppFlow
from googleapiclient.discovery      import build
from shutil                         import copyfile
from datetime                       import datetime
from io                             import BytesIO
from enum                           import Enum

class Backup:
    
    class Method(Enum):
        EXTERNAL_DRIVE  = 1
        CLOUD_DRIVE     = 2


    def __init__(self, file_name, config_file, **kwargs) -> None:
        self._filename                      = file_name

        # TODO: Pydantic model/validation for config
        self.config_path                    = Path(config_file)

        assert(self.config_path.exists())

        config_file                         = self.config_path.open()
        self.config                         = json.load(config_file)
        config_file.close()
        self.config_changed                 = False
        
        # External Drive
        self._external_drive_caching        = kwargs["external_drive_caching"] if "external_drive_caching" in kwargs else True 

        system = platform.system()
        if system == "Linux":
            self._local_file                = Path(f"{self.config['paths']['linux']['local']}{self._filename}")
            self._external_file             = Path(f"{self.config['paths']['linux']['external']}{self._filename}")
        elif system == "Windows":
            self._local_file                = Path(f"{self.config['paths']['windows']['local']}{self._filename}")
            self._external_file             = Path(f"{self.config['paths']['windows']['external']}{self._filename}")

        # Cloud
        self._cloud_caching                 = kwargs["cloud_caching"] if "cloud_caching" in kwargs else False

        if self._cloud_caching:
            self._drive_folder              = self.config["cloud"]["google"]["drive_folder"]                     


    def load(self):
        if self._external_drive_caching and self._cloud_caching:
            most_recent = self._get_most_recent_source()
            if most_recent == Backup.Method.EXTERNAL_DRIVE:
                self._load_file_from_external_drive()
            elif most_recent == Backup.Method.CLOUD_DRIVE:
                self._load_file_from_cloud()

        elif self._external_drive_caching:
            self._load_file_from_external_drive()

        elif self._cloud_caching:
            self._load_file_from_cloud()


    def _get_most_recent_source(self):
        service = self._create_service()

        try:
            folder_id = self.config["cloud"]["google"]["folder_id"]
        except KeyError:
            folder_id = self._get_folder_id(service)

        query = f"name='{self._filename}' and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="files(id, modifiedTime)").execute()
        file = response.get("files")[0]

        cloud_drive_ts = datetime.strptime(file["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
        external_drive_ts = self._external_file.stat().st_mtime

        if external_drive_ts >= cloud_drive_ts:
            return Backup.Method.EXTERNAL_DRIVE
        else:
            return Backup.Method.CLOUD_DRIVE

    
    def __del__(self):
        print("Shutting down..")
        if self._external_drive_caching:
            print(f"Writing to backup at {self._external_file}..")
            try:
                self._write_file_to_external_drive()
            except IOError as e:
                print("Could not write to external backup:")
                print(e)

        if self._cloud_caching:
            try:
                print("Writing to backup on Google Drive..")
                self._write_file_to_cloud()
            except HttpError as e:
                print("Could not write to Google Drive:")
                print(e)

        if self.config_changed:
            print(f"Updating {self.config_path} with new keys..")
            config_file = self.config_path.open("w")
            json.dump(self.config, config_file)
            config_file.close()


    """Raises IOError"""
    def _load_file_from_external_drive(self) -> None:
        if not self._local_file.exists():
            self._local_file.parent.mkdir()
            self._local_file.touch()

        if self._external_file.exists():
            if not self._local_file.exists() or self._local_file.stat().st_mtime < self._external_file.stat().st_mtime:
                copyfile(self._external_file, self._local_file)
        else:
            raise IOError(f"{self._external_file} does not exist. Can not load backup file.")


    """Raises IOError"""
    def _write_file_to_external_drive(self) -> None:
        if not self._external_file.parent.exists():
            try:
                self._external_file.parent.mkdir()
            except IOError as e:
                raise IOError(f"Could not access external storage device at {self._external_file}: {e}")

        copyfile(self._local_file, self._external_file)
        self._local_file.touch()


    def _get_folder_id(self, service) -> str:
        try:
            query = f"name='{self._drive_folder}'"
            response = service.files().list(q=query, fields="files(id)").execute()
            folder_id =  response.get("files")[0]["id"]
            self.config["cloud"]["google"]["folder_id"] = folder_id
            self.config_changed = True
            return folder_id

        except HttpError as e:
            print(e)
            folder_meta = {
                "name":     "databases",
                "mimeType": "application/vnd.google-apps.folder"
            }
            response = service.files().create(body=folder_meta, fields="id").execute()
            folder_id = response.get("id")
            self.config["cloud"]["google"]["folder_id"] = folder_id
            self.config_changed = True
            return folder_id


    """Raises HttpError"""
    def _load_file_from_cloud(self) -> None:
        service = self._create_service()

        try:
            folder_id = self.config["cloud"]["google"]["folder_id"]
        except KeyError:
            folder_id = self._get_folder_id(service)

        query = f"name='{self._filename}' and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="files(id, modifiedTime)").execute()
        file = response.get("files")[0]

        cloud_dt = datetime.strptime(file["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if cloud_dt.timestamp() > self._local_file.stat().st_mtime:
            request = service.files().get_media(fileId=file["id"])
            backup_file = BytesIO()
            downloader = MediaIoBaseDownload(backup_file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"{self._filename} download {int(status.progress() * 100)}% completed")

            with open(self._local_file, "wb") as localFile:
                localFile.write(backup_file.getbuffer())


    """Raises HttpError"""
    def _write_file_to_cloud(self) -> None:
        service = self._create_service()

        try:
            folder_id = self.config["cloud"]["google"]["folder_id"]
        except KeyError:
            folder_id = self._get_folder_id(service)


        file_metadata = { "name": f"{self._filename}", "parents": [folder_id] }
        media = MediaFileUpload(self._local_file)
        
        query = f"name='{self._filename}' and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="files(id)").execute()
        files = response.get("files")
        if files:
            service.files().update(media_body=media, fileId=files[0]["id"]).execute()
        else:
            service.files().create(body=file_metadata, media_body=media).execute()

        self._local_file.touch()

        
    def _create_service(self):
        CLIENT_SECRET_FILE  = self.config["cloud"]["google"]["client_secret_file"]
        API_SERVICE_NAME    = self.config["cloud"]["google"]["api_name"]
        API_VERSION         = self.config["cloud"]["google"]["api_version"]
        SCOPES              = self.config["cloud"]["google"]["scopes"]
        print(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES, sep=',')

        cred = None

        pickle_file = Path(f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle")

        if pickle_file.exists():
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(f"{API_SERVICE_NAME} service created successfully")
            return service
        except Exception as e:
            print(f"Unable to connect to Google API. {e}")
            return None
