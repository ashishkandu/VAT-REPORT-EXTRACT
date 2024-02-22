import json
from settings import DRIVE_CACHE_PATH
from drive_database.credential_handler import get_credentials
from drive_database.drive import GoogleDriveFile, retrive_latest_file_by_pattern, download_drive_file
from drive_database.database_operations import restore

creds = get_credentials()
# list_files(creds)


def perform_restore(file: GoogleDriveFile):
    if DRIVE_CACHE_PATH.exists():
        with DRIVE_CACHE_PATH.open('r') as f:
            info: dict = json.load(f)
        if info['name'] == file['name']:
            print("Database already restored from the latest backup!")
            return None
        else:
            print(
                f"Database was restored from another backup on {info['datetime']}")
            print(f"Current backup: {info['name']}")
            print(f"Latest backup: {file['name']}")
            choice = input("Do you want to restore latest backup? [y/N] ")
            if choice.lower() != 'y':
                return None
            print("Database will be restored from the latest backup!")

    filepath = download_drive_file(creds, file)
    restore(filepath)


if __name__ == '__main__':

    file_pattern = r"VatBillingSoftware_\d+_\d+\.bak"

    latest_file = retrive_latest_file_by_pattern(creds, file_pattern)
    if latest_file is not None:
        perform_restore(latest_file)
