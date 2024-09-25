# psaps
**p**hylogenetically **s**tandardized **a**ssessment of **p**angenome **s**ize / expansion associated metrics

<p align="center">
<img src="https://github.com/user-attachments/assets/0b19bb5d-e86c-41f4-82b5-e98672081d2f" width="300">
</p>

## Overview:

Understanding pangenome dynamics is critical for studying the emergence of pathogens or guiding natural products discovery. However, metrics for assessment of pangenome size or expansion rates or genome fluidity and make comparisons of them between different taxonomic or phylogenetic groups often do not account for differences in the phylogenetic diversity/breadth between groups. `psaps` provides a framework for performing this and standardizing such metrics to assess how open pangenomes are for different microbial species or clades by processing results from a comprehensive orthology inference and phylogenomic analyses.

For instance, suppose you have 5 bacterial species and you are interested in finding out whether the pangenome of one species is larger or expanding faster. First, you could run orthology prediction with all genomes and then identify core genes across the five species to use those to construct a core genome phylogeny. This will give you all the inputs you need to run `psaps`. You can also inform `psaps` which genome belongs to which species/group or you can say there should be 5 groups, and if they are well behaved species and are phylogenetically distinct, it should be able to parititon the genomes appropriately. 

For each group/species/clade, `psaps` will then prune the comprehensive phylogeny for only the genomes belonging to the group. This is done using ete3 (importantly with the option *preserve_branch_length* set to True). The summed branch lengths are then summed and used as a measure of core genome phylogenetic breadth to standardize metrics associated with pangenomes, which range from genome fluidity (as defined by Kislyuk et al. 2011) to simply total number of ortholog groups to auxiliary ortholog groups (computed as simply the total number of ortholog groups minus the number of loose core ortholog groups (ortholog groups present in >=80% of genomes).

## Info on Inputs:

* **OG_MATRIX**: The orthogroup matrix file should be a tab-delmited text file where rows correspond to orthogroups and columns to genomes. Then the values of the matrix indicate whether an orthogroup is found in a genome. Any value besides a blank `` or `0` indicates presence. *Note, the first cell in the matrix/table should be blank or feature a dummy value to make the matrix/table rectangular.*
* **SPECIES_TREE**: A comprehensive phylogeny of the genomes in the orthogroup matrix file, ideally constructed of a core genome alignment.
* **GROUP_MAP**: A tab-delimited file for mapping genome IDs (first column) to groups/clades (second column).
* **CLADE_COUNT**: If a group mapping file is not provided, Treemmmer (by Menardo et al. 2018) will be used to select X distinct representative genomes, where X can be adjusted by chaning this variable (default is 3). The rest of the genomes are then assigned to their closest representative genome based on phylogenetic distance to determine groups/clades.
* **PAIRWISE**: A flag to perform pairwise assessment of genomes instead of calculating stats across full subclades. Will also compute genome fluidity - which is exclusive to this mode.

## Info on Outputs:

* **track.txt**: The major output is simply a tab-delimited table reporting various metrics:
        * **group**: The group/clade identifier.
        * **genome_fluidity**: The genome fluidity metric per pair of genomes as defined by Kislyuk et al. 2011 - only computed in pairwise mode.
        * **genome_fluidity_standardized**: The genome fluidity metric per pair of genomes divided by the branch distance between the genomes along the core genome phylogeny - only computed in pairwise mode.
        * **samples**: The number of samples in the group.
        * **branch_sum**: The aggregate sum of the phylogeny pruned for genomes belonging to the group. 
        * **tot_ogs**: The number of total distinct ortholog groups found across the focal group.
        * **aux_ogs**: The number of auxiliary ortholog groups (total ortholog groups - core ortholog groups). 
        * **aux_prop**: The proportion of total ortholog groups which are auxiliary. 

* **psaps_plot.pdf**: A basic visualization of some results. If run without pairwise mode, the plot will be a scatterplot showing the relationship between aggregate branch lengths and distinct auxiliary ortholog groups for clades. If run in pairwise mode, then the plot will be show boxplots for each clade where values correspond to pairwise genome fluidity estimates standardized by phylogenetic distance.  

## Usage:

```
usage: psaps [-h] -m OG_MATRIX [-t SPECIES_TREE] [-g GROUP_MAP] [-k CLADE_COUNT] [-p] [-c CORE_GENOME] -o OUTDIR [-v]

        Program: psaps
        Author: Rauf Salamzade
        Affiliation: Kalan Lab, UW Madison, Department of Medical Microbiology and Immunology

        This program takes as input an ortholog matrix, a species tree, and either a:
        (1) mapping file grouping genomes to groupings or (2) count for the number of distinct
        phylogenomic groups to divide the genomes into using Treemmer with the input species
        tree.

        It then computes statistics related to pangenome size and also branch distances across
        subclades/groups of genomes by extracting/pruning them out of the global phylogeny.

        Genomic fluidity and standardized genomic fluidity are only computed in pairwise mode.


options:
  -h, --help            show this help message and exit
  -m OG_MATRIX, --og-matrix OG_MATRIX
                        Path to tab-delimited orthogroup matrix. Columns
                        should correspond to genome names and rows to
                        orthogroups, with blank cells and/or
                        cells with 0 indicating orthogroup
                        absence in a genome and everything else indicating
                        presence. First cell (first column, first row)
                        should be blank or filler.
  -t SPECIES_TREE, --species-tree SPECIES_TREE
                        Path to species tree in Newick format. Genome
                        labels should match column names in orthogroup
                        matrix.
  -g GROUP_MAP, --group-map GROUP_MAP
                        Path to tab-delimited file where the first column
                        corresponds to a genome name and the second
                        column to the group/clade identifier.
  -k CLADE_COUNT, --clade-count CLADE_COUNT
                        The number of distinct clades to partition
                        genomes into using Treemmer with the input species
                        tree [Default is 3].
  -p, --pairwise        Perform pairwise assessments between genomes.
  -c CORE_GENOME, --core-genome CORE_GENOME
                        The percentage of genomes an orthogroup needs to
                        be found in to be considered core [Default is 80.0].
  -o OUTDIR, --outdir OUTDIR
                        Path to output directory.
  -v, --version         Print version and exit.
```
