import requests
import tarfile
import os
import zipfile
from zipfile import ZipFile
import argparse

HOST = 'https://pypi.org'


def query_package(package_title: str) -> dict:
    httpr = requests.get(f'{HOST}/pypi/{package_title}/json')
    return httpr.json()


def get_source(query_response: dict) -> str:
    source_list = [items["url"] for items in query_response["urls"]]
    for url in source_list:
        if 'tar.gz' in url:
            return url
        return source_list[-1]


def get_package(package_address: str) -> str:
    file_title = package_address.split('/')[-1]
    r = requests.get(package_address, stream=True)
    with open(f'{file_title}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return file_title


def tar_py_files(members):
    for childinfo in members:
        if os.path.splitext(childinfo.name)[1] == ".py":
            yield childinfo


def run() -> None:
    parser = argparse.ArgumentParser(prog="Safepull",
                                     description="Extracts a package to the CWD without interfacing with setup.py")
    parser.add_argument('-p', '--package', help='Package title to be downloaded.')
    parser.add_argument('-f', '--force', action='store_true')
    args = parser.parse_args()
    use_in = args.package
    if not args.package:
        use_in = input('Input a package title: ')
    json_response = query_package(use_in)
    package_source = get_source(json_response)
    print(f'Package: {json_response["info"]["name"]}')
    print(f'Author: {json_response["info"]["author"]}')
    print(f'Download URL: {package_source}')
    if not args.force:
        use_in = input('Would you like to download and extract this package? (Y/N): ')
    if use_in.lower() == 'y' or args.force:
        file_loc = get_package(package_source)
        if file_loc.endswith('.tar.gz'):
            tar = tarfile.open(file_loc)
            tar.extractall(members=tar_py_files(tar))
            tar.close()
        if file_loc.endswith('.whl'):
            with ZipFile(file_loc) as whl_zip:
                zip_members = [my_member for my_member in whl_zip.namelist() if my_member.endswith('.py')]
                whl_zip.extractall(members=zip_members)
        os.remove(file_loc)
    print('All done! :)')


if __name__ == '__main__':
    run()
