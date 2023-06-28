# safepull

A quick and dirty command-line script to pull down and extract .py files out of tarballs and wheels without interfacing
with the setup.py file. This is a targeted replacement for `pip download <package>` to prevent malware detonation within
setup.py files. 

# Installation Instructions
Safepull is available on PyPI.

`pip install safepull`

# Usage Instructions
Safepull has three command line arguments.

Positional argument `<packagename>` is required. When force is not specified, you will be prompted for a distribution type to download.

`-f --force` will attempt to download the sdist of a particular package without prompt. 

`-m --metadata` will return the package name, description, and author of a particular package.

```
rem@rembox:~$ safepull numpy
numpy 1.24.3
Fundamental package for array computing in Python
Author: Travis E. Oliphant et al.
--0--
Filename: numpy-1.24.3-cp310-cp310-macosx_10_9_x86_64.whl
Package Type: bdist_wheel
URL: https://files.pythonhosted.org/packages/f3/23/7cc851bae09cf4db90d42a701dfe525780883ada86bece45e3da7a07e76b/numpy-1.24.3-cp310-cp310-macosx_10_9_x86_64.whl
Size: 19MB
```
