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
```
python format_proteomefile.py <foldername>
```

### Adding annotations
Sometimes it can happen that the reference genome does not contain annotations, meaning there are no annotations listed in the `Annotations` column. In that case you will need to add the annotations corresponding to the Accession Number. Do that **after** formatting the files. Only files with the extention `*_formatted.txt` can be annotated. Use the script `annotate.py` to replace the accession number with the annotations in the `Annotations` column. 

USAGE: 
```
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
 
Use the script `statistics.py` to merge the two files that need to be compared, determine all the necessary characteristics and statistics for plotting and add those numbers as new columns to the end of the files. The created file can then be used directly as input for the plotting scripts to generate the desired figures. 

USAGE: 
```
python statistics.py </path/input_filename_1/> </path/input_filename_2/>
```

The output files will have following filename: STRAIN_SHAREDPHASE_MEDIUM1VSMEDIUM2.txt or STRAIN_SHAREDMEDIUM_PHASE1_PHASE2.txt

## Plotting
Finally, the data can be plotted. The input file needs to have 25 columns, where the extension '_1' is condition 1, and '_2' is condition 2 (whatever is in the last part of the filename: 
`#_1     Annotation_1    Accession Number        1_1     2_1     3_1     Control_1       norms_1_1       norms_2_1       norms_3_1       #_2     Annotation_2    1_2     2_2     3_2     Control_2       norms_1_2             norms_2_2       norms_3_2       Row_Average_1   STD_1   Row_Average_2   STD_2   Log2_Fold_Change        Transformed_P_Value`

In case you followed the previous steps until now, the files you have should already be in the correct format (filename: STRAIN_SHAREDPHASE_MEDIUM1VSMEDIUM2.txt or STRAIN_SHAREDMEDIUM_PHASE1_PHASE2.txt).

There are two plots that can be generated with the provided scripts: 
1. XY-plots including a linear regression and computation of R**2 value.
2. Volcano plots (transformed p-value vs. log2 fold change)

Both scripts will create a figure in *pdf* and one in *html* format. The html file will allow you to look at your data in an interactive hover-over plot. When hovering over the points, the annotation will be displayed.

First create a new folder that you would like to store your figure files in. Use following scripts to create the plots: 
```
python xy_plot.py </path/input_filename.txt> </path/output_foldername/>
python volcano_plot.py </path/input_filename.txt> </path/output_foldername/>
```
Alternatively, you can loop over all the files that you would like to create the figures for with a for-loop such as the following one:
```
for file in /path/to/final/data/*.txt
do
    python xy_plot.py "$file" /path/to/FIGURES/
    python volcano_plot.py "$file" /path/to/FIGURES/
done
```

In addition to plotting the data as volcano and xy plots, the script `significant_list.py` allows you to extract all significantly overexpressed proteins (the ones that are above the threshold specified in the volcano plots = log2FC>±0.5, p-value>2) and save them as list in *.csv format. To run the script type: 

```
python significant_list.py </path/input_filename.txt> </path/output_foldername/>
```
or as for loop: 
```
for file in /path/to/final/data/*.txt
do
    python significant_list.py "$file" </path/output_foldername/>
done
```

**This is it! ENJOY YOUR DATA!**

