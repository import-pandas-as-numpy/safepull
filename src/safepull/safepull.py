import requests
import tarfile
import os
from zipfile import ZipFile
import argparse
from .models import Distribution, Package
from .exceptions import PackageNotFound

HOST = "https://pypi.org"


def query_package(package_title: str, version: str | None = None) -> Package:
    if version:
        response = requests.get(f"{HOST}/pypi/{package_title}/{version}/json").json()
    else:
        response = requests.get(f"{HOST}/pypi/{package_title}/json").json()
    try:
        my_package = Package(
            name=response["info"]["name"],
            summary=response["info"]["summary"],
            author=response["info"]["author"],
            version=response["info"]["version"],
            distributions=[
                Distribution.from_dict(releases) for releases in response["urls"]
            ],
        )
    except KeyError:
        raise PackageNotFound(package_title, version)
    return my_package


def unpack(file_loc: str) -> None:
    """Unpack a .tar.gz or .whl file into the CWD, and remove the compressed file.
    Arguments:
    file_loc -- the file title of a tarball or wheel in the current working directory.
    """
    if file_loc.endswith(".tar.gz"):
        tar = tarfile.open(file_loc)
        tar.extractall()
        tar.close()
    if file_loc.endswith((".whl", ".zip")):
        with ZipFile(file_loc) as whl_zip:
            whl_zip.extractall()
    os.remove(file_loc)


def run() -> None:
    parser = argparse.ArgumentParser(
        prog="Safepull",
        description="Extracts a package to the CWD without interfacing with setup.py",
    )
    parser.add_argument("package", help="Package title to be downloaded.")
    parser.add_argument(
        "-v", "--version", help="Version of a package to be downloaded."
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Automatically selects a download URL.",
    )
    parser.add_argument(
        "-m", "--metadata", action="store_true", help="Displays metadata on a package."
    )
    args = parser.parse_args()

    use_in = args.package
    if not args.package:
        use_in = input("Input a package title: ")

    user_package = query_package(use_in, args.version)
    print(*user_package.get_metadata(), sep="\n")
    if args.metadata:
        return
    if not args.force:
        if len(distribution_list := user_package.get_distributions()) > 1:
            for idx, distros in enumerate(distribution_list):
                print(f"--{idx}--", *distros.get_metadata(), sep="\n")
            while True:
                use_select = int(input("Enter the index of a package to download: "))
                try:
                    file_name = distribution_list[use_select].download_package()
                    unpack(file_name)
                    break
                except (KeyError, TypeError, IndexError):
                    print("Invalid Selection.")
        else:
            distros = user_package.get_distributions()
            print(*distros[0].get_metadata())
            if input("Download package? (Y/N):").lower() == "y":
                file_name = distros[0].download_package()
                unpack(file_name)
    else:
        sdist = user_package.get_sdist()
        if sdist is None:
            print("No sdist found. Grabbing first package.")
            sdist = user_package.get_distributions()[0]
        file_name = sdist.download_package()
        unpack(file_name)
