"""
Unit test for corpus to Alpino converter.
"""

import difflib
import glob
import unittest
import tempfile
import os
import shutil

from chamd.__main__ import main


class TestChamd(unittest.TestCase):
    """
    Unit test class.
    """

    def test_chamd(self):
        """
        Test that sentences are converted to the expected output.
        """

        data_dir = os.path.dirname(__file__)
        test_files = glob.glob(os.path.join(data_dir, '*.cha'))
        expected_files = glob.glob(os.path.join(data_dir, '*.txt'))

        # Currently CHAMD only works on physical files in a directory.
        # To deal with this, the test files will be copied to a
        # temporary location and the parse will be performed there.
        with tempfile.TemporaryDirectory() as tmpdir:
            for test_file in test_files:
                shutil.copy(test_file, tmpdir)
            main(['-p', tmpdir,
                  '--outpath', tmpdir,
                  '-c', os.path.join(tmpdir, 'charmap.txt')])
            actual_files = glob.glob(
                os.path.join(tmpdir, '**', '*.txt'), recursive=True)

            for expected_file in expected_files:
                basename = os.path.basename(expected_file)
                for actual_file in actual_files:
                    if os.path.basename(actual_file) == basename:
                        with open(actual_file) as handle:
                            actual_lines = handle.readlines()
                        with open(expected_file) as handle:
                            expected_lines = handle.readlines()
                        diff_lines = list(difflib.context_diff(
                            expected_lines,
                            actual_lines,
                            basename + ' (expected)',
                            basename + ' (actual)'))
                        if len(diff_lines) > 0:
                            self.fail(''.join(diff_lines))
