import logging
from datetime import datetime
import json
from pathlib import Path
from typing import Optional, TypedDict
import io
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from src.loggerfactory import LoggerFactory

from settings import DRIVE_CACHE_PATH


logger = LoggerFactory.get_logger(__name__)


class GoogleDriveFile(TypedDict):
    kind: str
    mimeType: str
    id: str
    name: str


def list_files(credentials: Credentials):
    logger.info("Listing files from Google Drive...")

    # Build the Google Drive service using the obtained credentials
    service = build('drive', 'v3', credentials=credentials)

    # Example: List files in Google Drive
    results = service.files().list(pageSize=10, fields="files(name)").execute()
    files = results.get('files', [])

    if not files:
        logger.info('No files found.')
    else:
        print('Files:')
        for file in files:
            print(file['name'])


def retrive_latest_file_by_pattern(credentials: Credentials, file_pattern: str) -> Optional[GoogleDriveFile]:
    """
    Retrieve the latest file from Google Drive that matches the specified pattern.

    Args:
    - credentials: The credentials for accessing Google Drive API.
    - file_pattern: The pattern to match the file name.

    Returns:
    - The metadata of the latest matching file, or None if no file is found.
    """
    logger.info(f"Retrieving the latest file by pattern: {file_pattern}")
    # Build the Google Drive service using the obtained credentials
    service = build('drive', 'v3', credentials=credentials)

    query = "trashed=false"

    results = service.files().list(
        q=query,
        orderBy="modifiedTime desc",
    ).execute()

    items = results.get('files', [])

    # Validate the file pattern
    try:
        re.compile(file_pattern)
    except re.error:
        logger.error(f"Invalid regular expression pattern: '{file_pattern}'")
        return None

    # Filter files by the specified pattern
    matching_items = [file for file in items if re.search(
        file_pattern, file['name'])]

    if not matching_items:
        logger.info(f"No file matching the pattern '{file_pattern}' found.")
        return None

    logger.debug(f"Total matching files: {len(matching_items)}")

    latest_file = matching_items[0]

    return latest_file


def download_drive_file(credentials: Credentials, drive_file: GoogleDriveFile):
    """
    Download a file from Google Drive.

    Args:
        credentials (Credentials): The credentials to authenticate the Google Drive API.
        drive_file (GoogleDriveFile): The file to be downloaded from Google Drive.

    Returns:
        Path: The path to the downloaded file.

    Raises:
        None
    """
    logger.info(f"Downloading Google Drive file: {drive_file['name']}")
    service = build('drive', 'v3', credentials=credentials)

    # Download the drive file
    request = service.files().get_media(fileId=drive_file['id'])

    file_path = Path('/backup') / drive_file['name']

    if file_path.exists():
        logger.info(f"File already exists: {file_path}")
        cache_it(drive_file)
        return file_path

    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        logger.info(f"Downloaded {int(status.progress() * 100)}%")

    file_path.write_bytes(file.getvalue())
    logger.info(f"File write complete {file_path}")

    cache_it(drive_file)

    return file_path


logger = logging.getLogger(__name__)


def cache_it(drive_file: GoogleDriveFile):
    """
    Caches information about the drive file.

    Args:
        drive_file (GoogleDriveFile): The drive file to cache information about.
    """
    logger.info("Caching information about the drive file...")

    try:
        with DRIVE_CACHE_PATH.open('w', encoding='utf-8') as f:
            content = {
                'datetime': datetime.now().isoformat(),
                'name': drive_file['name']
            }
            json.dump(content, f)
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Error occurred during file operation: {e}")
