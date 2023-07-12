[![Python package](https://github.com/UUDigitalHumanitieslab/chamd/actions/workflows/python-package.yml/badge.svg?branch=develop)](https://github.com/UUDigitalHumanitieslab/chamd/actions/workflows/python-package.yml)
[![Python package](https://badge.fury.io/py/chamd.svg)](https://pypi.python.org/pypi/chamd/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8091301.svg)](https://doi.org/10.5281/zenodo.8091301)
# CHAMD
Conversion and cleaning of CHILDES CHA files into PaQu Plaintext
Metadata Format (to convert to Alpino).

## Installation and usage
```bash
pip install chamd
chamd --help
```

Running from project:
```bash
python -m chamd --help
```

## Import as library
This way the library can be used to read CHAT file (contents) from an external application.

```python
from chamd import ChatReader
reader = ChatReader()
chat = reader.read_file('example.cha') # or read_string

for item in chat.metadata:
    print(item)
for line in chat.lines:
    for item in line.metadata:
        print(item)
    print(line.text)
```

## Upload to PyPi
```bash
python setup.py sdist
twine upload dist/*
```

## Run tests
```bash
python -m unittest discover tests/
```