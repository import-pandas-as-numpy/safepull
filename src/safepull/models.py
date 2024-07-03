"""Class models used by Safepull."""

from dataclasses import dataclass
from io import BytesIO

import requests
from humanize import naturalsize
from rich.table import Table


@dataclass
class Distribution:
    """Dataclass containing distribution information for a PyPI package."""

    filename: str
    packagetype: str
    url: str
    size: int

    @classmethod
    def from_dict(cls, releases: dict):
        """Create a distribution from JSON."""
        return cls(
            filename=releases["filename"],
            packagetype=releases["packagetype"],
            url=releases["url"],
            size=releases["size"],
        )

    def download_package(self) -> tuple[BytesIO, str]:
        """Download a compressed package."""
        r = BytesIO(requests.get(self.url, stream=True, timeout=60).content)
        return r, self.filename

    def get_metadata(self) -> tuple[str, str, str, str]:
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
    def from_dict(cls, package_dict: dict):
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

    def get_metadata(self) -> tuple[str, str, str]:
        """Return pertinent metadata for the package."""
        return f"{self.name} {self.version}", self.summary, f"Author: {self.author}"

    def get_distributions(self) -> list[Distribution]:
        """Return a list of distributions."""
        return self.distributions

    def get_sdist(self) -> Distribution | None:
        """Extract the source distribution if it exists."""
        for distro in self.distributions:
            if distro.packagetype == "sdist":
                return distro
        return None

    def table_print(self) -> Table:
        """Rich table printing for distribution information."""
        table = Table(
            title=f"{self.name} v.{self.version}\nAuthor: {self.author}\n{self.summary}",  # noqa: E501
        )
        table.add_column("Index")
        table.add_column("Filename")
        table.add_column("Package Type")
        table.add_column("Size (MB)")
        for ind, entries in enumerate(self.distributions):
            table.add_row(
                str(ind),
                entries.filename,
                entries.packagetype,
                naturalsize(entries.size),
            )
        return table
