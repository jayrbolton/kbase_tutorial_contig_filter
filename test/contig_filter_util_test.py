import os
import unittest

from contig_filter_util import contig_filter


class ContigFilterUtilTest(unittest.TestCase):

    def test_contig_filter_ok(self):
        input_path = os.path.join('test', 'data', 'input.fasta')
        filtered_path = os.path.join('test', 'data', 'output.fasta')
        min_length = 500000
        out = contig_filter(input_path, filtered_path, min_length)
        self.assertEqual(out['n_total'], 2)
        self.assertEqual(out['n_remaining'], 1)
        self.assertTrue(os.path.exists(filtered_path))
