#!/usr/bin/env python3

'''
This script is used to format proteome files such that they are suitable for running in with the scripts 'proteome_data_vis' and 'volcano_plots'. 
The files downloaded from scaffold are '.xls' files and contain a header and two lines at the end of the file which need to be removed prior to uploading the data. After removing the header and footer, save the files as *.txt file (tab delimited) and upload them to your desired folder. The file should have 12 columns, the number of rows can be variable. Column names are: \ # \ Visible? \ Identifited Proteins(XXXX) \ Accession Number \ Alternate ID \ Molecular Weight \ Protein Grouping Ambiguity \ Taxonomy \ CONTROL \ REPLICATE_1 \ REPLICATE_2 \ REPLICATE_3 \

Make sure that the annotations are listed under Identified Proteins. If there are no annotions but accession numbers instead, use the script 'annotate.py' to replace the accession number with the annotations. 

USAGE: python format_proteomefile.py <foldername>
'''

import glob
import os
import sys

def format_proteomefiles(folder=''):
    
    selected_columns = [1, 3, 4, 9, 10, 11, 12]

    for filepath in glob.glob(os.path.join(folder, '*.txt')):
        filename = os.path.basename(filepath)  # Get the filename
        print(f"Processing file: {filename}")
        
        # Read the original file
        with open(filepath, 'r') as file:
            lines = file.readlines()
       
        # First, rename columns such that they are compatible with the scripts.
        header = lines[0].strip().split('\t')
        if len(header) == 13:
                header[3] = 'Annotation'
                header[9] = '1'
                header[10] = '2'
                header[11] = '3'
                header[12] = 'Control'

        # Filter selected columns for the header
        filtered_header = [header[i] for i in selected_columns]
        renamed_lines = ['\t'.join(filtered_header) + '\n']
        
        # Read in new header and combine with the filtered columns to be written to a new file
        for line in lines[1:]:
            columns = line.strip().split('\t')
            filtered_columns = [columns[i] for i in selected_columns]
            renamed_lines.append('\t'.join(filtered_columns) + '\n')
        
        # Sort by accession number (index 1 in the filtered columns)
        sorted_lines = renamed_lines[:1] + sorted(renamed_lines[1:], key=lambda x: x.split('\t')[1])
        
        # Write the sorted and filtered lines back to a new file
        output_file_path = filepath.replace('.txt', '_formatted.txt')
        
        with open(output_file_path, 'w') as file:
            file.writelines(sorted_lines)
        
        print(f"Formatted file written to: {output_file_path}")

if __name__ == "__main__": 
    
    if len(sys.argv) !=2: # If there is more than 1 argument to call this script, it will provide guidance on how to use it.
        print("Usage: python format_proteomefile.py <input_foldername>")
        sys.exit(1)
    
    folder = sys.argv[1]
    format_proteomefiles(folder)
