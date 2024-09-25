# psaps
**p**hylogenetically **s**tandardized **a**ssessment of  **p**angenome **s**ize / expansion

<p align="center">
<img src="https://github.com/user-attachments/assets/0b19bb5d-e86c-41f4-82b5-e98672081d2f" width="300">
</p>

## Usage

```
usage: psaps [-h] -m OG_MATRIX [-t SPECIES_TREE] [-g GROUP_MAP] [-k CLADE_COUNT] [-p] [-c CORE_GENOME] -o OUTDIR [-v]

        Program: psaps
        Author: Rauf Salamzade
        Affiliation: Kalan Lab, UW Madison, Department of Medical Microbiology and Immunology

        This program takes as input an ortholog matrix, a species tree, and either a:
        (1) mapping file grouping genomes to groupings or (2) count for the number of distinct
        phylogenomic groups to divide the genomes into using Treemmer with the input species
        tree.


options:
  -h, --help            show this help message and exit
  -m OG_MATRIX, --og-matrix OG_MATRIX
                        Path to tab-delimited orthogroup matrix. Columns should correspond to genome names and rows to orthogroups, with blank cells and/or cells with 0 indicating orthogroup absence in a genome and everything else indicating presence. First cell (first column, first row) should be blank or filler.
  -t SPECIES_TREE, --species-tree SPECIES_TREE
                        Path to species tree in Newick format. Genome labels should match column names in orthogroup matrix.
  -g GROUP_MAP, --group-map GROUP_MAP
                        Path to tab-delimited file where the first column corresponds to a genome name and the second column to the group/clade identifier.
  -k CLADE_COUNT, --clade-count CLADE_COUNT
                        The number of distinct clades to partition genomes into using Treemmer with the input species tree [Default is 3].
  -p, --pairwise        Perform pairwise assessments between genomes.
  -c CORE_GENOME, --core-genome CORE_GENOME
                        The percentage of genomes an orthogroup needs to be found in to be considered core [Default is 80.0].
  -o OUTDIR, --outdir OUTDIR
                        Path to output directory.
  -v, --version         Print version and exit.
```
