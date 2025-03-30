"""Unit tests for the Distribution and Package models in the safepull library."""

from safepull.models import Distribution, Package

# ruff: noqa: D103, S101, PLR2004


def test_distribution_from_dict() -> None:
    data = {
        "filename": "example.tar.gz",
        "packagetype": "sdist",
        "url": "https://example.com/example.tar.gz",
        "size": 1024,
    }
    distribution = Distribution.from_dict(data)
    assert distribution.filename == "example.tar.gz"
    assert distribution.packagetype == "sdist"
    assert distribution.url == "https://example.com/example.tar.gz"
    assert distribution.size == 1024


def test_distribution_get_metadata() -> None:
    distribution = Distribution(
        filename="example.tar.gz",
        packagetype="sdist",
        url="https://example.com/example.tar.gz",
        size=1024,
    )
    metadata = distribution.get_metadata()
    assert metadata == (
        "Filename: example.tar.gz",
        "Package Type: sdist",
        "URL: https://example.com/example.tar.gz",
        "Size: 0MB",
    )


def test_package_from_dict() -> None:
    data = {
        "info": {
            "name": "example-package",
            "summary": "An example package",
            "author": "John Doe",
            "version": "1.0.0",
        },
        "urls": [
            {
                "filename": "example.tar.gz",
                "packagetype": "sdist",
                "url": "https://example.com/example.tar.gz",
                "size": 1024,
            },
        ],
    }
    package = Package.from_dict(data)
    assert package.name == "example-package"
    assert package.summary == "An example package"
    assert package.author == "John Doe"
    assert package.version == "1.0.0"
    assert len(package.distributions) == 1
    assert package.distributions[0].filename == "example.tar.gz"


def test_package_get_metadata() -> None:
    package = Package(
        name="example-package",
        summary="An example package",
        author="John Doe",
        version="1.0.0",
        distributions=[],
    )
    metadata = package.get_metadata()
    assert metadata == (
        "example-package 1.0.0",
        "An example package",
        "Author: John Doe",
    )


def test_package_get_distributions() -> None:
    distribution = Distribution(
        filename="example.tar.gz",
        packagetype="sdist",
        url="https://example.com/example.tar.gz",
        size=1024,
    )
    package = Package(
        name="example-package",
        summary="An example package",
        author="John Doe",
        version="1.0.0",
        distributions=[distribution],
    )
    distributions = package.get_distributions()
    assert len(distributions) == 1
    assert distributions[0].filename == "example.tar.gz"


def test_package_get_sdist() -> None:
    sdist = Distribution(
        filename="example.tar.gz",
        packagetype="sdist",
        url="https://example.com/example.tar.gz",
        size=1024,
    )
    wheel = Distribution(
        filename="example.whl",
        packagetype="bdist_wheel",
        url="https://example.com/example.whl",
        size=2048,
    )
    package = Package(
        name="example-package",
        summary="An example package",
        author="John Doe",
        version="1.0.0",
        distributions=[sdist, wheel],
    )
    result = package.get_sdist()
    assert result == sdist

    package_no_sdist = Package(
        name="example-package",
        summary="An example package",
        author="John Doe",
        version="1.0.0",
        distributions=[wheel],
    )
    result = package_no_sdist.get_sdist()
    assert result is None
