#!/usr/bin/env python3

'''
This script is used to replace Accession Numbers with Annotations in the column `Identified Proteins (XXX)` / `Annotations`. 

USAGE: python annotate.py <foldername>
'''

import pandas as pd
import glob

def annotate_DSS3(input='', output_filename=''):
  with open(input, 'r') as input_file:\n
      with open(output_filename, 'w') as output_file:\n
      # Write the header line to the output file
        header = input_file.readline().strip() + '\\tAnnotation_Uniprot\\n'
        output_file.write(header)
      # Process each line in the input file
        for line in input_file:
      # Split the line into columns
          columns = line.strip().split('\\t')
          spo_id = columns[3]  # Extract the SPO ID from column 4
      # Look up the annotation in the dictionary\n",
          annotation = SPO_dict.get(spo_id, 'Unknown')\n",
      # Append the annotation to the end of the line and write to the output file\n",
          output_line = '\\t'.join(columns) + '\\t' + annotation + '\\n'
          output_file.write(output_line)


