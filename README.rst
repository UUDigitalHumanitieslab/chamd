[![Python package](https://github.com/UUDigitalHumanitieslab/chamd/actions/workflows/python-package.yml/badge.svg?branch=develop)](https://github.com/UUDigitalHumanitieslab/chamd/actions/workflows/python-package.yml)

Conversion and cleaning of CHILDES CHA files into PaQu Plaintext
Metadata Format (to convert to Alpino).

`pypi chamd
<https://pypi.org/project/chamd/>`_

.. code:: bash

   pip install chamd
   chamd --help

Running from project:

.. code:: bash

    python -m chamd --help

Import as Library
=================

This way the library can be used to read CHAT file (contents) from an external application.

.. code:: python

    from chamd import ChatReader
    reader = ChatReader()
    chat = reader.read_file('example.cha') # or read_string
    
    for item in chat.metadata:
        print(item)
    for line in chat.lines:
        for item in line.metadata:
            print(item)
        print(line.text)


Upload to PyPi
==============

.. code:: bash

   python setup.py sdist
   twine upload dist/*

Run Tests
=========

.. code:: bash

    python -m unittest discover tests/
