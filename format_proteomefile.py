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
    
    selected_columns = [0, 2, 3, 8, 9, 10, 11]
    
    for files in glob.glob(folder + '*.txt'):
        filename = file.split('/')[-1] #define the filename 
        # Read the original file
        with open(folder+filename, 'r') as file:
            lines = files.readlines()
        
        # First, rename columns such that they are compatible with the scripts.
        # Process each line and rename columns
        renamed_lines = []
        for line in lines:
            # Split the line into columns based on tab delimiter
            columns = line.strip().split('\t')
            print(columns)
            
            # Rename columns
            if len(columns) == 13:
                columns[3] = 'Annotation'
                columns[9] = '1'
                columns[10] = '2'
                columns[11] = '3'
                columns[12] = 'Control'

            # Filter selected columns
            filtered_columns = [columns[i] for i in selected_columns]
            print(filtered_columns)
            
            # Join the filtered columns back into a line
            processed_line = '\t'.join(filtered_columns) + '\n'
            renamed_lines.append(processed_line)
            
            # Join the columns back into a line
            renamed_line = '\t'.join(columns) + '\n'
            renamed_lines.append(renamed_line)
            print(renamed_lines)

        # Sort by accession number
        sorted_lines = sorted(renamed_lines, key=lambda x: x.split('\t')[3])  
        print(sorted_lines)
        
        
        # Write the sorted and filtered lines back to a new file
        output_file_path = file_path.replace('.txt', '_formatted.txt')
        print(output_file_path)
        
        with open(output_file_path, 'w') as file:
            file.writelines(sorted_lines)

        # CONTROL line: 
        print(f"Formatted file written to: {output_file_path}")

if __name__ == "__main__": 
    
    if len(sys.argv) !=2: # If there is more than 1 argument to call this script, it will provide guidance on how to use it.
        print("Usage: python format_proteomefile.py <input_foldername>")
        sys.exit(1)
'''
    for frame, translation in translation_dict.items(): 
            output_list.append(frame + '\t' + translation) # fill list with frame tab delimited with the respective translation from the translation_dict (= output of six-frame-tranlation.py)
        full_output = '\n'.join(output_list) # define full_output, so we separate each frame + translation into new lines. 

        outfilename = output_file

        with open(outfilename, 'w') as f: # write the frame + translation into new file with user specified filename.
            f.write(full_output)
'''
