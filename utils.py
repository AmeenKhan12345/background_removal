from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def upload_to_drive(file_path, file_name):
    """
    Uploads a file to Google Drive and returns a public URL.

    Args:
        file_path (str): Path to the file to be uploaded.
        file_name (str): Name to be given to the file on Google Drive.

    Returns:
        str: Public URL of the uploaded file.
    """
    try:
        # Ensure the file exists locally
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Authenticate Google Drive
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        # Create and upload the file
        file = drive.CreateFile({'title': file_name})
        file.SetContentFile(file_path)
        file.Upload()

        # Make the file publicly accessible
        file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})

        # Return the public URL
        return file['alternateLink']
    except Exception as e:
        raise Exception(f"Failed to upload file to Google Drive: {str(e)}")
