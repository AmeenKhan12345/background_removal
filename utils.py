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
        gauth.LoadClientConfigFile("client_secrets.json")
        gauth.LoadCredentialsFile("credentials.json")

        if gauth.credentials is None:
            print("No valid credentials found. Please authenticate...")
            gauth.LocalWebserverAuth()  # Will prompt user to authenticate
        elif gauth.access_token_expired:
            print("Credentials expired. Re-authenticating...")
            gauth.Refresh()
        else:
            print("Using existing credentials.")

        # Save credentials for future use
        gauth.SaveCredentialsFile("credentials.json")

        # Create the Drive client
        drive = GoogleDrive(gauth)

        # Create and upload the file
        file = drive.CreateFile({'title': file_name})
        file.SetContentFile(file_path)
        file.Upload()
        print(f"File {file_name} uploaded successfully to Google Drive.")

        # Make the file publicly accessible
        print("Setting file permissions to public...")
        file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
        print("File permissions set to public.")

        # Generate the correct public URL
        file.FetchMetadata()  # Refresh the file metadata to ensure permissions are updated
        public_url = f"https://drive.google.com/uc?export=view&id={file['id']}"
        print(f"Public URL: {public_url}")
        return public_url

    except Exception as e:
        print(f"Failed to upload file to Google Drive: {str(e)}")
        raise
