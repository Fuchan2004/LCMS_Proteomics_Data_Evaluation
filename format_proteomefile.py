#!/usr/bin/env python3

'''
This script is used to format proteome files such that they are suitable for running in with the scripts 'proteome_data_vis' and 'volcano_plots'. 
The files downloaded from scaffold are '.xls' files and contain a header and two lines at the end of the file which need to be removed prior to uploading the data. After removing the header and footer, save the files as *.txt file (tab delimited) and upload them to your desired folder. The file should have 12 columns, the number of rows can be variable. Column names are: \ # \ Visible? \ Identifited Proteins(XXXX) \ Accession Number \ Alternate ID \ Molecular Weight \ Protein Grouping Ambiguity \ Taxonomy \ CONTROL \ REPLICATE_1 \ REPLICATE_2 \ REPLICATE_3 \

Make sure that the annotations are listed under Identified Proteins. If there are no annotions but accession numbers instead, use the script 'annotate.py' to replace the accession number with the annotations. 

USAGE: 
'''

import glob
import os
import sys

def format_proteomefiles(folder=''):
    
    selected_columns = [0, 2, 3, 8, 9, 10, 11]
    
    for files in glob.glob(folder + '*.txt'):
        # Read the original file
        with open(files, 'r') as file:
            lines = files.readlines()
        
        # First, rename columns such that they are compatible with the scripts.
        # Process each line and rename columns
        renamed_lines = []
        for line in lines:
            # Split the line into columns based on tab delimiter
            columns = line.strip().split('\t')
            
            # Rename columns
            if len(columns) == 12:
                columns[2] = 'Annotation'
                columns[8] = 'Control'
                columns[9] = '1'
                columns[10] = '2'
                columns[11] = '3'

            # Filter selected columns
            filtered_columns = [columns[i] for i in selected_columns]
            
            # Join the filtered columns back into a line
            processed_line = '\t'.join(filtered_columns) + '\n'
            renamed_lines.append(processed_line)
            
            # Join the columns back into a line
            renamed_line = '\t'.join(columns) + '\n'
            renamed_lines.append(renamed_line)

        # Sort by accession number
        sorted_lines = sorted(renamed_lines, key=lambda x: x.split('\t')[3])  
        
        
        # Write the sorted and filtered lines back to a new file
        output_file_path = file_path.replace('.txt', '_formatted.txt')
        
        with open(output_file_path, 'w') as file:
            file.writelines(sorted_lines)

        # CONTROL line: 
        print(f"Formatted file written to: {output_file_path}")

if __name__ == "__main__": 
    
    if len(sys.argv) !=1: # If there is more than 1 argument to call this script, it will provide guidance on how to use it.
        print("Usage: python format_proteomefile.py <foldername>")
        sys.exit(1)
