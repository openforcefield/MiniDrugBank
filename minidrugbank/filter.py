# This is a python script to see if there is something to import travis will stop complaining.
from openeye import oechem
from openforcefield.utils import *

def print_smiles(file_name):
    molecules = read_molecules(file_name)
    for mol in molecules:
        print(oechem.OECreateIsoSmiString(mol))
    return
