import requests
import hashlib
import subprocess
import os

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    file_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    msg = requests.get(file_url)
    # Check whether the download was successful
    if msg.status_code == requests.codes.ok:
    # Extract text file content from response message
        filecontents = msg.text.split()
        hash = filecontents[0]
        return hash

def download_installer():
    file_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = requests.get(file_url)
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
    # Extract binary file content from response message body
        execontent = resp_msg.content
    # Calculate SHA-256 hash value
    return execontent

def installer_ok(installer_data, expected_sha256):
    if expected_sha256 == hashlib.sha256(installer_data).hexdigest():
        return True
    else:
        return False

def save_installer(installer_data):
    path = r'C:\Users\TBif\Desktop\vlcsetup.exe'
    with open(path, 'wb') as file:
        file.write(installer_data)
    return path

def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'])
    return
    
def delete_installer(installer_path):
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()