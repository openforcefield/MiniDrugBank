from unittest import TestCase
from openforcefield.utils import read_molecules
from openeye import oechem

class TestMiniDrugBank(TestCase):
    def test_repeating_molecules(self):
        """
        Test methods used to create minidrugbank
        """
        ff_mols = read_molecules('../MiniDrugBank_ff.mol2')
        tripos_mols = read_molecules('../MiniDrugBank_tripos.mol2')
        smiles = set()
        # check for repeating SMILES
        for idx, ff_mol in enumerate(ff_mols):
            # get SMILES information
            ff_smile = oechem.OECreateIsoSmiString(ff_mol)
            tri_mol = tripos_mols[idx]
            tri_smile = oechem.OECreateIsoSmiString(tri_mol)

            # SMILES should be the same for the two force fields
            self.assertEqual(ff_smile, tri_smile, msg = "SMILES for tripos molecule %s and parm@frosst molecule % should agree and don't" % (tri_mol.GetTitle(), ff_mol.GetTitle))

            # there should also be no repeating smiles
            self.assertFalse( (ff_smile in smiles), msg = "Found repeating SMILES string for %s" % ff_mol.GetTitle())

            # add smiles to the list
            smiles.add(ff_smile)

    #TODO
    #def test_3Dcoordinates(self):
