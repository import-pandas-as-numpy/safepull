"""Exceptions raised by Safepull."""


class PackageNotFoundError(Exception):
    """Raised when a package is not found.

    This relies on the use of the KeyError raised by
    parsing the JSON response.
    """

    def __init__(self, package_title: str, package_version: str | None) -> None:
        """Initialize the superclass with the appropriate information."""
        self.package_title = package_title
        self.package_version = package_version
        super().__init__(
            f"Package {self.package_title} v{self.package_version} not found.",
        )
