## Test Case

Inputs used for psaps analysis of fungal clades in our manuscript are provided here and psaps can be rerun as we did in the manuscript using the following command:

> [!IMPORTANT]
> Uncompress the file `Full_Orthogroup_Matrix.txt.gz` before running the command.
 
```
psaps -m Full_Orthogroup_Matrix.txt -t IQTree_SCC.treefile -g Clade_Mapping.txt -o psaps_pairwise_results/ -p
```

> The timing of this command should be around 1.75 minutes.
