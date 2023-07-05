class PackageNotFound(Exception):
    """
    Exception raised when a key error is encountered
    during processing of JSON data from PyPI's JSON API.
    """

    def __init__(self, package_title: str, package_version: str | None):
        self.package_title = package_title
        self.package_version = package_version
        super().__init__(
            f"Package {self.package_title} v{self.package_version} not found."
        )
