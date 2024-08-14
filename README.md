# LCMS_Proteomics_Data_Evaluation
This repository contains instructions and code to plot x/y treatment plots and volcano plots of proteomics results obtained from Scaffold. 

*Copyright Fadime Stemmer*

## Prerequisites and file formatting
### Conda Environment
The environment necessary to run the pipeline can be created from the 'environment.yaml' file in this repository. The enviornment name is `MS_plot`: 

`conda envs create -f environment.yaml`

Once the environment is done building, check that the new environment was installed correctly:

`conda info --envs`

Activate the environment: 

`conda activate MS_plot`

### Pre-formatting
The files downloaded from scaffold are `.xls` files and contain a header and two lines at the end of the file (one empty line, second line containing the string 'END OF FILE') which need to be removed prior to uploading the data. After removing the header and footer, save the files as *.txt file (tab delimited) and upload them to your desired folder. The file should have 12 columns, the number of rows can be variable. Column names are: 

`\ # \ Visible? \ Identifited Proteins(XXXX) \ Accession Number \ Alternate ID \ Molecular Weight \ Protein Grouping Ambiguity \ Taxonomy \ CONTROL \ REPLICATE_1 \ REPLICATE_2 \ REPLICATE_3 \`

### Adding annotations
Sometimes it can happen that the reference genome does not contain annotations, meaning there are no annotations listed in the `Identified proteins (XXX)` column. In that case you will need to add the annotations corresponding to the Accession Number. Use the script `annotate.py` to replace the accession number with the annotations in the `Identified proteins (XXX)` column. 

USAGE: 

### Formatting files
To create volcano plots and xy plots from your Scaffold output, the files need to be in a specific format to run with this code. The script `format_proteomefile.py` can be used to format the files in the desired way. Essentially what it does is: 
1. Select the columns used in the analysis (= removing columns that are redundant) and save them to a new file. 
2. Rename the columns `Identified Proteins` into `Annotations`
3. Rename the columns containing the data (Control + Biological Triplicates) into `Control, 1, 2, 3`
4. Sort the lines by Accession Number

The new file will be saved as *filename*`_formatted.txt`

USAGE: `python format_proteomefile.py <foldername>`
