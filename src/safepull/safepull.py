"""Safepull module for the safe handling of compressed Python scripts."""

# ruff: noqa: T201

import argparse
import tarfile
from io import BytesIO
from os import chdir
from pathlib import Path
from zipfile import ZipFile

import requests
from rich.console import Console

from .models import Package

HOST = "https://pypi.org"


def query_package(package_title: str, version: str | None = None) -> Package:
    """Query PyPI for a package."""
    if version:
        response = requests.get(
            f"{HOST}/pypi/{package_title}/{version}/json",
            timeout=60,
        )
    else:
        response = requests.get(f"{HOST}/pypi/{package_title}/json", timeout=60)
    response.raise_for_status()
    return Package.from_dict(response.json())


def unpack(byte_object: BytesIO, filename: str) -> None:
    """Unpack a compressed file into the CWD."""
    if filename.endswith(".tar.gz"):
        with tarfile.open(fileobj=byte_object) as sdist_tar:
            if hasattr(tarfile, "data_filter"):
                sdist_tar.extractall(filter="data")
            else:
                print(
                    "You do not have data filters enabled for your Python version.",
                    "This may present a security risk of path traversal.",
                    sep="\n",
                )
                if input('To ignore this, enter "Y": ').upper() == "Y":
                    sdist_tar.extractall()
    if filename.endswith((".whl", ".zip")):
        with ZipFile(byte_object) as whl_zip:
            whl_zip.extractall(path=Path.cwd().joinpath(f"{filename[:-4]}"))


def run() -> None:
    """Run the program."""
    console = Console()
    parser = argparse.ArgumentParser(
        prog="Safepull",
        description="Extracts a package to the CWD without interfacing with setup.py",
    )
    parser.add_argument("package", help="Package title to be downloaded.")
    parser.add_argument(
        "-v",
        "--version",
        help="Version of a package to be downloaded.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Automatically selects a download URL.",
    )
    parser.add_argument(
        "-m",
        "--metadata",
        action="store_true",
        help="Displays metadata on a package.",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Downloads all distributions of a package.",
    )
    args = parser.parse_args()

    use_in = args.package
    if not args.package:
        use_in = input("Input a package title: ")

    user_package = query_package(use_in, args.version)

    if args.all:
        root_folder = Path(f"{user_package.name}-{user_package.version}/")
        root_folder.mkdir(exist_ok=True)
        chdir(root_folder)
        for distro in user_package.get_distributions():
            print(f"Downloading {distro.filename}...")
            byteobject, file_name = distro.download_package()
            unpack(byteobject, file_name)
        return
    if args.metadata:
        print(*user_package.get_metadata(), sep="\n")
        return
    if not args.force:
        if len(distribution_list := user_package.get_distributions()) > 1:
            console.print(user_package.table_print())
            while True:
                use_select = int(input("Enter the index of a package to download: "))
                byteobject, file_name = distribution_list[use_select].download_package()
                unpack(byteobject, file_name)
                break
        else:
            distros = user_package.get_distributions()
            print(*distros[0].get_metadata())
            if input("Download package? (Y/N):").lower() == "y":
                byteobject, file_name = distros[0].download_package()
                unpack(byteobject, file_name)
    else:
        sdist = user_package.get_sdist()
        if sdist is None:
            print("No sdist found. Grabbing first package.")
            sdist = user_package.get_distributions()[0]
        byteobject, file_name = sdist.download_package()
        unpack(byteobject, file_name)
