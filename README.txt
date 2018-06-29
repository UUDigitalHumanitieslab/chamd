Conversion and cleaning of CHILDES CHA files into PaQu Plaintext
Metadata Format (to convert to Alpino).

.. code:: bash

   pip install chamd
   chamd --help

Running from project:

.. code:: bash

   python -m chamd --help

Upload to PyPi
==============

.. code:: bash

   python setup.py sdist
   twine upload dist/*
