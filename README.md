# MiniDrugBank

This repository is used to distribute the MiniDrugBank molecule set, filtered from [DrugBank Release Version 5.0.1](http://www.drugbank.ca/releases/latest)

## Installation

Install `MiniDrugBank` via conda:
```bash
conda install -c mobleylab minidrugbank=0.0.0
```

If you wish to use the Jupyter notebook `MiniDrugBank/pickMolecules.ipynb` you will also need `openforcefield` tools available on github at [openforcefield/openforcefield](https://github.com/openforcefield/openforcefield)

## Building MiniDrugBank

This molecule set was created for the purpose of [smarty and smirky](https://github.com/openforcefield/smarty) tools for sampling chemical perception. The goal was to maintain the chemical complexity in the DrugBank database with as few molecules as possible. First we removed molecules based on the following criteria:

* contained metal or metaloid atoms
* had less than 3 or more than 100 heavy atoms
* could not be assigned parm@frosst atom types
    - Note this doesn't mean all molecules can be assigned parm@frosst force field parameters as it is possible that all combinations of atom types were not available in that force field.
* were assigned generic parameters (`n1`, `b1`, `a1`, or `t1`) with [SMIRNOFF99Frosst](https://github.com/openforcefield/smirnoff99Frosst)

Next the minimum molecules that kept the same diversity in parm@frosst atom types and smirnoff99Frosst parameter types were stored.

### Citing DrugBank

* Law V, Knox C, Djoumbou Y, Jewison T, Guo AC, Liu Y, Maciejewski A, Arndt D, Wilson M, Neveu V, Tang A, Gabriel G, Ly C, Adamjee S, Dame ZT, Han B, Zhou Y, Wishart DS. DrugBank 4.0: shedding new light on drug metabolism. Nucleic Acids Res. 2014 Jan 1;42(1):D1091-7.[24203711](https://www.ncbi.nlm.nih.gov/pubmed/24203711)
* Knox C, Law V, Jewison T, Liu P, Ly S, Frolkis A, Pon A, Banco K, Mak C, Neveu V, Djoumbou Y, Eisner R, Guo AC, Wishart DS. DrugBank 3.0: a comprehensive resource for 'omics' research on drugs. Nucleic Acids Res. 2011 Jan;39(Database issue):D1035-41.[21059682](https://www.ncbi.nlm.nih.gov/pubmed/21059682)
* Wishart DS, Knox C, Guo AC, Cheng D, Shrivastava S, Tzur D, Gautam B, Hassanali M. DrugBank: a knowledgebase for drugs, drug actions and drug targets. Nucleic Acids Res. 2008 Jan;36(Database issue):D901-6.[18048412](https://www.ncbi.nlm.nih.gov/pubmed/18048412)
* Wishart DS, Knox C, Guo AC, Shrivastava S, Hassanali M, Stothard P, Chang Z, Woolsey J. DrugBank: a comprehensive resource for in silico drug discovery and exploration. Nucleic Acids Res. 2006 Jan 1;34(Database issue):D668-72.[16381955](https://www.ncbi.nlm.nih.gov/pubmed/16381955)

