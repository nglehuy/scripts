import requests
from progress.spinner import PixelSpinner as Spinner
import sys

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        sp = Spinner("Downloading ... ")
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                sp.next()

def download(url, fileid, destination):
    session = requests.Session()

    response = session.get(url, params={ 'id': fileid }, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': fileid, 'confirm': token}
        response = session.get(url, params = params, stream=True)

    save_response_content(response, destination)

if __name__ == '__main__':
    download(sys.argv[1], sys.argv[2], sys.argv[3])
