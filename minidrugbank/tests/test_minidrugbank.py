from unittest import TestCase
import os
import pytest
from pkg_resources import resource_filename
from openforcefield.utils import read_molecules
from openforcefield.typing.engines.smirnoff.forcefield import ForceField
from openeye import oechem

def test_in_tests():
    print("WE GOT IN A TEST SECTION!!!!")

class TestMiniDrugBank(TestCase):
    basepath = os.path.dirname(__file__)
    tri_file = os.path.abspath(os.path.join(basepath, '..', 'MiniDrugBank_tripos.mol2'))
    if not os.path.exists(tri_file):
        raise Exception("%s tripos file not found" % tri_file)
    ff_file = os.path.abspath(os.path.join(basepath, '..', 'MiniDrugBank_ff.mol2'))
    if not os.path.exists(ff_file):
        raise Exception("%s parm@frosst file not found" % ff_file)
    tripos_mols = read_molecules(tri_file)
    ff_mols = read_molecules(ff_file)

    def test_repeating_molecules(self):
        """
        Test methods used to create minidrugbank
        """
        smiles = set()
        # check for repeating SMILES
        for idx, ff_mol in enumerate(TestMiniDrugBank.ff_mols):
            # get SMILES information
            ff_smile = oechem.OECreateIsoSmiString(ff_mol)
            tri_mol = TestMiniDrugBank.tripos_mols[idx]
            tri_smile = oechem.OECreateIsoSmiString(tri_mol)

            # SMILES should be the same for the two force fields
            self.assertEqual(ff_smile, tri_smile, msg = "SMILES for tripos molecule %s and parm@frosst molecule % should agree and don't" % (tri_mol.GetTitle(), ff_mol.GetTitle))

            # there should also be no repeating smiles
            self.assertFalse( (ff_smile in smiles), msg = "Found repeating SMILES string for %s" % ff_mol.GetTitle())

            # add smiles to the list
            smiles.add(ff_smile)

    def test_atom_types(self):
        """
        Check the number of atom types represented hasn't changed
        """
        atom_types = {1: [12, set()], 6: [12, set()], 7: [8, set()],
                8: [5, set()], 9: [1, set()], 15: [1, set()], 16: [5, set()],
                17: [1, set()], 35: [1, set()], 53: [1, set()]}

        for mol in TestMiniDrugBank.ff_mols:
            for atom in mol.GetAtoms():
                # get atomic number
                n = atom.GetAtomicNum()
                t = atom.GetType()
                self.assertTrue(n in atom_types, msg = "Atomic number %i not in original set" % n)
                atom_types[n][1].add(t)

        # Check that the number of types here match original
        for n, [count, s] in atom_types.items():
            self.assertTrue( len(s) == count, msg = "Current set has %i atom types for atomic number %i, there were %i in the original set" % (len(s), n, count))

    def test_pid_types(self):
        """
        Check that the number of smirnoff parameter types hasn't changed
        """
        pids = {'HarmonicBondGenerator': [73, set()],
                'HarmonicAngleGenerator': [34, set()],
                'PeriodicTorsionGenerator': [136, set()],
                'NonbondedGenerator': [26, set()]}

        ffxml = resource_filename('smirnoff99frosst', 'smirnoff99Frosst.ffxml')
        ff = ForceField(ffxml)
        #ff = ForceField("forcefield/smirnoff99Frosst.ffxml")
        labels = ff.labelMolecules(TestMiniDrugBank.ff_mols, verbose = False)
        # loop through labels from smirnoff
        for force_dict in labels:
            for force, label_list in force_dict.items():
                for (indics, pid, smirks) in label_list:
                    # we don't have current counts on impropers
                    if pid[0] == 'i':
                        continue
                    pids[force][1].add(pid)

        # Check that the number of types here match original
        for force, [count, s] in pids.items():
            self.assertTrue( len(s) == count, msg = "Current set has %i types for the force %s, there were %i in the original set" % (len(s), force, count))

    def test_3Dcoordinates(self):
        """
        Check for three dimensional coordinates for every molecule
        """
        for idx, ff_mol in enumerate(TestMiniDrugBank.ff_mols):
            tri_mol = TestMiniDrugBank.tripos_mols[idx]
            self.assertTrue(ff_mol.GetDimension()==3, msg="Molecule %s in parm@frosst set doesn't have 3D coordinates" % ff_mol.GetTitle())
            self.assertTrue(tri_mol.GetDimension()==3, msg="Molecule %s in tripos set doesn't have 3D coordinates" % tri_mol.GetTitle())


    def test_check_hydrogens(self):
        """
        Test that explicit hydrogens are already included on all molecules
        In other words the implicit hydrogen count on all atoms is zero
        """
        for mol in TestMiniDrugBank.tripos_mols:
            for a in mol.GetAtoms():
                self.assertTrue(a.GetImplicitHCount() == 0, msg = "Found a %i atom with implicit hydrogens" % a.GetAtomicNum())

