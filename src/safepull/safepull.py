from typing import Iterator

import requests
import tarfile
import os
from zipfile import ZipFile
import argparse
from dataclasses import dataclass

HOST = 'https://pypi.org'


@dataclass
class Distribution:
    """Dataclass containing distribution information for a PyPI package."""
    filename: str
    packagetype: str
    url: str
    size: int

    @classmethod
    def from_dict(cls, releases: dict):
        return cls(filename=releases['filename'],
                   packagetype=releases['packagetype'],
                   url=releases['url'],
                   size=releases['size'])

    def download_package(self) -> str:
        r = requests.get(self.url, stream=True)
        with open(f'{self.filename}', 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        return self.filename

    def get_metadata(self) -> tuple[str, str, str, str]:
        return (f'Filename: {self.filename}',
                f'Package Type: {self.packagetype}',
                f'URL: {self.url}',
                f'Size: {self.size / (1 << 20):,.0f}MB')


@dataclass
class Package:
    """Dataclass containing PyPI package metadata."""
    name: str
    summary: str
    author: str
    version: str
    distributions: list[Distribution]

    def get_metadata(self) -> tuple[str, str, str]:
        return (f'{self.name} {self.version}',
                self.summary,
                f'Author: {self.author}')

    def get_distributions(self) -> list[Distribution]:
        return self.distributions

    def get_sdist(self) -> Distribution | None:
        for distro in self.distributions:
            if distro.packagetype == 'sdist':
                return distro
        return None


def query_package(package_title: str) -> Package:
    response = requests.get(f'{HOST}/pypi/{package_title}/json').json()
    return Package(name=response['info']['name'],
                   summary=response['info']['summary'],
                   author=response['info']['author'],
                   version=response['info']['version'],
                   distributions=[Distribution.from_dict(releases) for releases in response["urls"]])


def tar_py_files(members: tarfile.TarFile) -> Iterator[tarfile.TarInfo]:
    """Generator function to yield .py file members in tarballs.
    Arguments:
    members -- a tarfile to iterate over.
    Yields:
    childinfo -- a tarinfo object with a .py suffix."""
    for childinfo in members:
        if os.path.splitext(childinfo.name)[1] == ".py":
            yield childinfo


def unpack(file_loc: str) -> None:
    """Unpack a .tar.gz or .whl file into the CWD, and remove the compressed file.
    Arguments:
    file_loc -- the file title of a tarball or wheel in the current working directory.
    """
    if file_loc.endswith('.tar.gz'):
        tar = tarfile.open(file_loc)
        tar.extractall(members=tar_py_files(tar))
        tar.close()
    if file_loc.endswith('.whl'):
        with ZipFile(file_loc) as whl_zip:
            zip_members = [my_member for my_member in whl_zip.namelist() if my_member.endswith('.py')]
            whl_zip.extractall(members=zip_members)
    os.remove(file_loc)


def run() -> None:
    parser = argparse.ArgumentParser(prog="Safepull",
                                     description="Extracts a package to the CWD without interfacing with setup.py")
    parser.add_argument('package', help='Package title to be downloaded.')
    parser.add_argument('-f', '--force', action='store_true', help='Automatically selects a download URL.')
    parser.add_argument('-m', '--metadata', action='store_true', help='Displays metadata on a package.')
    args = parser.parse_args()

    use_in = args.package
    if not args.package:
        use_in = input('Input a package title: ')

    user_package = query_package(use_in)
    print(*user_package.get_metadata(), sep='\n')
    if args.metadata:
        return
    if not args.force:
        if len(distribution_list := user_package.get_distributions()) > 1:
            for idx, distros in enumerate(distribution_list):
                print(f'--{idx}--', *distros.get_metadata(), sep='\n')
            while True:
                use_select = int(input('Enter the index of a package to download: '))
                try:
                    file_name = distribution_list[use_select].download_package()
                    unpack(file_name)
                    break
                except (KeyError, TypeError, IndexError):
                    print('Invalid Selection.')
        else:
            distros = user_package.get_distributions()
            print(*distros[0].get_metadata())
            if input('Download package? (Y/N):').lower() == 'y':
                file_name = distros[0].download_package()
                unpack(file_name)
    else:
        sdist = user_package.get_sdist()
        if sdist is None:
            print('No sdist found. Grabbing first package.')
            sdist = user_package.get_distributions()[0]
        file_name = sdist.download_package()
        unpack(file_name)
