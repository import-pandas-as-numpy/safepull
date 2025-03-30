"""Unit tests for the safepull module."""

import argparse
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from safepull.models import Package
from safepull.safepull import query_package, run, unpack


@pytest.fixture()
def mock_package() -> MagicMock:
    """Fixture to create a mock Package object."""
    mock_pkg = MagicMock(spec=Package)
    mock_pkg.name = "example-package"
    mock_pkg.version = "1.0.0"
    mock_pkg.get_distributions.return_value = [
        MagicMock(
            filename="example-1.0.0.tar.gz",
            download_package=MagicMock(
                return_value=(BytesIO(b"data"), "example-1.0.0.tar.gz"),
            ),
        ),
        MagicMock(
            filename="example-1.0.0.whl",
            download_package=MagicMock(
                return_value=(BytesIO(b"data"), "example-1.0.0.whl"),
            ),
        ),
    ]
    mock_pkg.get_sdist.return_value = mock_pkg.get_distributions()[0]
    mock_pkg.get_metadata.return_value = ["Metadata line 1", "Metadata line 2"]
    mock_pkg.table_print.return_value = "Mocked Table"
    return mock_pkg


@patch("safepull.safepull.requests.get")
def test_query_package(mock_get: MagicMock, mock_package: MagicMock) -> None:
    """Test the query_package function."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"name": "example-package", "version": "1.0.0"}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    with patch("safepull.safepull.Package.from_dict", return_value=mock_package):
        result = query_package("example-package")
        assert result == mock_package  # noqa: S101
        mock_get.assert_called_once_with(
            "https://pypi.org/pypi/example-package/json",
            timeout=60,
        )


@patch("safepull.safepull.tarfile.open")
@patch("safepull.safepull.ZipFile")
def test_unpack(mock_zipfile: MagicMock, mock_tarfile: MagicMock) -> None:
    """Test the unpack function."""
    # Test .tar.gz file
    mock_tar = MagicMock()
    mock_tarfile.return_value.__enter__.return_value = mock_tar
    byte_object = BytesIO(b"data")
    unpack(byte_object, "example-1.0.0.tar.gz")
    mock_tar.extractall.assert_called_once()

    # Test .whl file
    mock_zip = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip
    unpack(byte_object, "example-1.0.0.whl")
    mock_zip.extractall.assert_called_once_with(
        path=Path.cwd().joinpath("example-1.0.0"),
    )


@patch("safepull.safepull.query_package")
@patch("safepull.safepull.unpack")
@patch("safepull.safepull.Path.mkdir")
@patch("safepull.safepull.chdir")
@patch("safepull.safepull.Console.print")
@patch("safepull.safepull.input", side_effect=["0", "y"])
def test_run(  # noqa: PLR0913
    mock_input: MagicMock,  # noqa: ARG001
    mock_console_print: MagicMock,
    mock_chdir: MagicMock,
    mock_mkdir: MagicMock,
    mock_unpack: MagicMock,
    mock_query_package: MagicMock,
    mock_package: MagicMock,
) -> None:
    """Test the run function."""
    mock_query_package.return_value = mock_package

    # Test --all flag
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            package="example-package",
            version=None,
            force=False,
            metadata=False,
            all=True,
        ),
    ):
        run()
        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_chdir.assert_called_once()
        mock_unpack.assert_called()

    # Reset mock_unpack call count
    mock_unpack.reset_mock()

    # Test --metadata flag
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            package="example-package",
            version=None,
            force=False,
            metadata=True,
            all=False,
        ),
    ):
        run()
    # Reset mock_unpack call count
    mock_unpack.reset_mock()
    # Test interactive selection
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            package="example-package",
            version=None,
            force=False,
            metadata=False,
            all=False,
        ),
    ):
        run()
        mock_console_print.assert_called_once_with("Mocked Table")
        mock_unpack.assert_called_once()
