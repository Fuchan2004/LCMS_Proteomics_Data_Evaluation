# LCMS_Proteomics_Data_Evaluation
This repository contains instructions and code to plot x/y treatment plots and volcano plots of proteomics results obtained from Scaffold. 

Copyright Fadime Stemmer

## Prerequisites and file formatting
The files downloaded from scaffold are '.xls' files and contain a header and two lines at the end of the file (one empty line, second line containing the string 'END OF FILE') which need to be removed prior to uploading the data. After removing the header and footer, save the files as *.txt file (tab delimited) and upload them to your desired folder. The file should have 12 columns, the number of rows can be variable. Column names are: \ # \ Visible? \ Identifited Proteins(XXXX) \ Accession Number \ Alternate ID \ Molecular Weight \ Protein Grouping Ambiguity \ Taxonomy \ CONTROL \ REPLICATE_1 \ REPLICATE_2 \ REPLICATE_3 \

Make sure that the annotations are listed under 'Identified Proteins'. If there are no annotions but accession numbers instead, use the script 'annotate.py' to replace the accession number with the annotations (see instructions below). 

### Adding annotations

### Formatting files
To create volcano plots and xy plots from your Scaffold output, the files need to be in a specific format to run with this code. The script 'format_proteomefile.py' can be used to format the files in the desired way. Essentially what it does is: 
