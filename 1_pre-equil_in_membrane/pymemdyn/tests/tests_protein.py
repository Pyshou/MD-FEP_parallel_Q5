import protein

import os
import unittest

class TestMonomerProtein(unittest.TestCase):

    def setUp(self):
        self.pdb = "tests/monomer.pdb"

    def test_monomer_load(self):
        '''Check the correct loading of a simple monomer
        '''
        monomer = protein.Monomer(pdb = self.pdb)

        self.assertIsInstance(monomer, protein.Monomer)

    def test_monomer_his_normalization(self):
        '''After loading, the protein HIS are normalized by default.
        Check that the file exist'''
        
        monomer = protein.Monomer(pdb = self.pdb)

        self.assertTrue(os.path.isfile("tests/monomer-his.pdb"))

    def test_monomer_has_no_chain(self):
        '''Some proteins can have a chain defined, which breaks pdb2gmx.
        Test that our monomer has no chain defined'''

        with open(self.pdb, "r") as monomer_file:
            for line in monomer_file:
                if line.startswith("ATOM"):
                    self.assertTrue(line[21] == " ")

if __name__ == "__main__":
    unittest.main()
