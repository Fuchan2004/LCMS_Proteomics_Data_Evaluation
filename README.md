# LCMS_Proteomics_Data_Evaluation
This repository contains instructions and code to plot x/y treatment plots and volcano plots of proteomics results obtained from Scaffold. 

*Copyright Fadime Stemmer*

## Prerequisites and file formatting
### Conda Environment
The environment necessary to run the pipeline can be created from the 'environment.yaml' file in this repository. The enviornment name is `MS_plot`: 

```
conda envs create -f environment.yaml
```

Once the environment is done building, check that the new environment was installed correctly:

```
conda info --envs
```

Activate the environment: 

```
conda activate MS_plot
```

### Pre-formatting
The files downloaded from scaffold are `.xls` files and contain a header and two lines at the end of the file (one empty line, second line containing the string 'END OF FILE') which need to be removed prior to uploading the data. After removing the header and footer, save the files as *.txt file (tab delimited) and upload them to your desired folder. The file name must have following format: **DATE_STRAIN_MEDIUM_GROWTHPHASE.txt** The file should have 12 columns, the number of rows can be variable. Column names are: 

`\ # \ Visible? \ Identifited Proteins(XXXX) \ Accession Number \ Alternate ID \ Molecular Weight \ Protein Grouping Ambiguity \ Taxonomy \ CONTROL \ REPLICATE_1 \ REPLICATE_2 \ REPLICATE_3 \`

### Formatting files
To create volcano plots and xy plots from your Scaffold output, the files need to be in a specific format to run with this code. The script `format_proteomefile.py` can be used to format the files in the desired way. Essentially what it does is: 
1. Select the columns used in the analysis (= removing columns that are redundant) and save them to a new file. 
2. Rename the columns `Identified Proteins` into `Annotations`
3. Rename the columns containing the data (Control + Biological Triplicates) into `Control, 1, 2, 3`
4. Sort the lines by Accession Number

The new file will be saved as *filename*`_formatted.txt`

USAGE: 
```python
python format_proteomefile.py <foldername>
```

### Adding annotations
Sometimes it can happen that the reference genome does not contain annotations, meaning there are no annotations listed in the `Annotations` column. In that case you will need to add the annotations corresponding to the Accession Number. Do that **after** formatting the files. Only files with the extention `*_formatted.txt` can be annotated. Use the script `annotate.py` to replace the accession number with the annotations in the `Annotations` column. 

USAGE: 
```python
python annotate.py </path/annotations_file.txt> </path/input_foldername/>
```

**Now we are ready to get started with the evaluation of our proteomes!**

## Statistics
The data typically consisting of biological triplicates need to be evaluated statistically. Specifically:
- *For the x-y-plots* 
  1. we calcualte the mean value of the triplicate measurements to plot against the mean of the treatment to be compared to
  2. we need to determine the standard deviation to plot as error bars
 
- *For the volcano-plots*
  1. we determine the log2 fold change
  2. we need the -log(p-value) to determine whether the changes/differences are significant or not.
 
Use the script `statistics.py` to merge the two files that need to be compared, determine all the necessary characteristics and statistics for plotting and add those numbers as new columns to the end of the files. The created file can then be used directly as input for the plotting scripts to generate the desired figures. USAGE: 
```python
python statistics.py </path/input_filename_1/> </path/input_filename_2/>
```

### Plotting

