from dataclasses import dataclass
import requests


@dataclass
class Distribution:
    """Dataclass containing distribution information for a PyPI package."""

    filename: str
    packagetype: str
    url: str
    size: int

    @classmethod
    def from_dict(cls, releases: dict):
        return cls(
            filename=releases["filename"],
            packagetype=releases["packagetype"],
            url=releases["url"],
            size=releases["size"],
        )

    def download_package(self) -> str:
        r = requests.get(self.url, stream=True)
        with open(f"{self.filename}", "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        return self.filename

    def get_metadata(self) -> tuple[str, str, str, str]:
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

    def get_metadata(self) -> tuple[str, str, str]:
        return f"{self.name} {self.version}", self.summary, f"Author: {self.author}"

    def get_distributions(self) -> list[Distribution]:
        return self.distributions

    def get_sdist(self) -> Distribution | None:
        for distro in self.distributions:
            if distro.packagetype == "sdist":
                return distro
        return None
