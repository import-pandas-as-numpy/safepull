"""Class models used by Safepull."""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

import requests


@dataclass
class Distribution:
    """Dataclass containing distribution information for a PyPI package."""

    filename: str
    packagetype: str
    url: str
    size: int

    @classmethod
    def from_dict(cls: type[Self], releases: dict) -> Self:
        """Create a distribution from JSON."""
        return cls(
            filename=releases["filename"],
            packagetype=releases["packagetype"],
            url=releases["url"],
            size=releases["size"],
        )

    def download_package(self: Self) -> str:
        """Download a compressed package to the current working directory."""
        r = requests.get(self.url, stream=True, timeout=60)
        with Path(self.filename).open(mode="wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        return self.filename

    def get_metadata(self: Self) -> tuple[str, str, str, str]:
        """Return the metadata for a specific distribution of a package."""
        return (
            f"Filename: {self.filename}",
            f"Package Type: {self.packagetype}",
            f"URL: {self.url}",
            f"Size: {self.size / (1 << 20):,.0f}MB",
        )


@dataclass
class Package:
    """Dataclass containing PyPI package metadata."""

    name: str
    summary: str
    author: str
    version: str
    distributions: list[Distribution]

    @classmethod
    def from_dict(cls: type[Self], package_dict: dict) -> Self:
        """Create a Package class from JSON."""
        return cls(
            name=package_dict["info"]["name"],
            summary=package_dict["info"]["summary"],
            author=package_dict["info"]["author"],
            version=package_dict["info"]["version"],
            distributions=[
                Distribution.from_dict(releases) for releases in package_dict["urls"]
            ],
        )

    def get_metadata(self: Self) -> tuple[str, str, str]:
        """Return pertinent metadata for the package."""
        return f"{self.name} {self.version}", self.summary, f"Author: {self.author}"

    def get_distributions(self: Self) -> list[Distribution]:
        """Return a list of distributions."""
        return self.distributions

    def get_sdist(self: Self) -> Distribution | None:
        """Extract the source distribution if it exists."""
        for distro in self.distributions:
            if distro.packagetype == "sdist":
                return distro
        return None
