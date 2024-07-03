# safepull

Safepull is a command line tool to interact with PyPI's package indexing to safely download and extract files. This is a targeted replacement for `pip download <package>` to prevent malware detonation within
setup.py files.

## Installation Instructions

Safepull is available on PyPI.

`pip install safepull`

## Usage Instructions

Safepull has four command line arguments.

Positional argument `<packagename>` is required. When force is not specified, you will be prompted for a distribution type to download.

`-f --force` will attempt to download the sdist of a particular package without prompt.

`-v --version` will attempt to download a specific version of a particular package.

`-m --metadata` will return the package name, description, and author of a particular package.

`-a --all` will download *all* distributions of a given package/version combination.

```plaintext
py -m safepull numpy
                                                  numpy v.1.25.0
                                         Author: Travis E. Oliphant et al.
                                 Fundamental package for array computing in Python
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Index ┃ Filename                                                                     ┃ Package Type ┃ Size (MB) ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 0     │ numpy-1.25.0-cp310-cp310-macosx_10_9_x86_64.whl                              │ bdist_wheel  │ 19.13     │
│ 1     │ numpy-1.25.0-cp310-cp310-macosx_11_0_arm64.whl                               │ bdist_wheel  │ 13.32     │
│ 2     │ numpy-1.25.0-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl    │ bdist_wheel  │ 13.48     │
│ 3     │ numpy-1.25.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl      │ bdist_wheel  │ 16.80     │
│ 4     │ numpy-1.25.0-cp310-cp310-musllinux_1_1_x86_64.whl                            │ bdist_wheel  │ 16.64     │
│ 5     │ numpy-1.25.0-cp310-cp310-win32.whl                                           │ bdist_wheel  │ 12.02     │
│ 6     │ numpy-1.25.0-cp310-cp310-win_amd64.whl                                       │ bdist_wheel  │ 14.34     │
│ 7     │ numpy-1.25.0-cp311-cp311-macosx_10_9_x86_64.whl                              │ bdist_wheel  │ 19.11     │
│ 8     │ numpy-1.25.0-cp311-cp311-macosx_11_0_arm64.whl                               │ bdist_wheel  │ 13.33     │
│ 9     │ numpy-1.25.0-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl    │ bdist_wheel  │ 13.47     │
│ 10    │ numpy-1.25.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl      │ bdist_wheel  │ 16.79     │
│ 11    │ numpy-1.25.0-cp311-cp311-musllinux_1_1_x86_64.whl                            │ bdist_wheel  │ 16.65     │
│ 12    │ numpy-1.25.0-cp311-cp311-win32.whl                                           │ bdist_wheel  │ 12.02     │
│ 13    │ numpy-1.25.0-cp311-cp311-win_amd64.whl                                       │ bdist_wheel  │ 14.33     │
│ 14    │ numpy-1.25.0-cp39-cp39-macosx_10_9_x86_64.whl                                │ bdist_wheel  │ 19.16     │
│ 15    │ numpy-1.25.0-cp39-cp39-macosx_11_0_arm64.whl                                 │ bdist_wheel  │ 13.34     │
│ 16    │ numpy-1.25.0-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl      │ bdist_wheel  │ 13.51     │
│ 17    │ numpy-1.25.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl        │ bdist_wheel  │ 16.84     │
│ 18    │ numpy-1.25.0-cp39-cp39-musllinux_1_1_x86_64.whl                              │ bdist_wheel  │ 16.67     │
│ 19    │ numpy-1.25.0-cp39-cp39-win32.whl                                             │ bdist_wheel  │ 12.05     │
│ 20    │ numpy-1.25.0-cp39-cp39-win_amd64.whl                                         │ bdist_wheel  │ 14.36     │
│ 21    │ numpy-1.25.0-pp39-pypy39_pp73-macosx_10_9_x86_64.whl                         │ bdist_wheel  │ 18.51     │
│ 22    │ numpy-1.25.0-pp39-pypy39_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.whl │ bdist_wheel  │ 16.22     │
│ 23    │ numpy-1.25.0-pp39-pypy39_pp73-win_amd64.whl                                  │ bdist_wheel  │ 14.23     │
│ 24    │ numpy-1.25.0.tar.gz                                                          │ sdist        │ 9.94      │
└───────┴──────────────────────────────────────────────────────────────────────────────┴──────────────┴───────────┘
```
