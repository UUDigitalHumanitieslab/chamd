Conversion and cleaning of CHILDES CHA files into PaQu Plaintext Metadata Format (to convert to Alpino).

```bash
pip install chamd
chamd --help
```

Running from project:

```bash
python -m chamd --help
```

# Upload to PyPi

```bash
python setup.py sdist
twine upload dist/*
```
