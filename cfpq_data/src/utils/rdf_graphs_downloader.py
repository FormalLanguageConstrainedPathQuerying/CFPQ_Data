import requests
from tqdm import tqdm

from cfpq_data.src.utils.utils import add_graph_dir


# TODO: rewrite to work with Google API
def download_file_from_google_drive(file_id, destination):
    download_file_prefix = 'https://docs.google.com/uc?export=download'

    session = requests.Session()

    response = session.get(download_file_prefix, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(download_file_prefix, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    chunk_size = 32768

    with open(destination, 'wb') as f:
        for chunk in tqdm(response.iter_content(chunk_size), desc='Downloading'):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download_data(graph_group, graph_name, graph_key):
    dst = add_graph_dir(graph_group)

    arch_dst = dst / f'{graph_name}.tar.xz'

    download_file_from_google_drive(graph_key, arch_dst)

    return dst
