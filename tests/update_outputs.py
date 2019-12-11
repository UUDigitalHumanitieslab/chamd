"""
Unit test for corpus to Alpino converter.
"""

import difflib
import glob
import unittest
import tempfile
import os
import shutil
import sys

data_dir = os.path.dirname(__file__)

# import this implementation
sys.path.insert(0, os.path.join(data_dir, ".."))

from chamd.__main__ import main

test_files = glob.glob(os.path.join(data_dir, '*.cha'))

print(test_files)

# Perform CHAMD only on physical files in a directory.
# Copy output back and overwrite any existing expected output files
with tempfile.TemporaryDirectory() as tmpdir:
    for test_file in test_files:
        shutil.copy(test_file, tmpdir)
    main(['-p', tmpdir,
            '--outpath', tmpdir,
            '-c', os.path.join(tmpdir, 'charmap.txt'),
            '--verbose'])

    actual_files = glob.glob(
        os.path.join(tmpdir, '**', '*.txt'))

    for output in actual_files:
        shutil.copy(output, os.path.abspath(data_dir))
