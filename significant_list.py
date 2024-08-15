#!/usr/bin/env python3

'''
This script is used to extract the significant values (log2 fold change > 0.5 & -log10(p-value) >2) from the proteome data. 

USAGE: python significant.py </path/input_filename> </path/output_folder/>
'''

import pandas as pd
import sys
import os

def significant_list(title, log2_fold_change, transformed_pvalues, annotations, accessions, output_path):
    # Create lists to store the significant points and their annotations
    sign_plus = []
    sign_minus = []
    accession_sign_plus = []
    accession_sign_minus = []

    for i in range(len(log2_fold_change)):
        if transformed_pvalues[i] > 2:
            if log2_fold_change[i] > 0.5:
                sign_plus.append(annotations[i])
                accession_sign_plus.append(accessions[i])
                sign_minus.append(None)  # No value for underexpressed in this case
                accession_sign_minus.append(None)
            elif log2_fold_change[i] < -0.5:
                sign_plus.append(None)  # No value for overexpressed in this case
                accession_sign_plus.append(None)
                sign_minus.append(annotations[i])
                accession_sign_minus.append(accessions[i])
            else:
                # Not adding anything if the log2 fold change is between -0.5 and 0.5
                sign_plus.append(None)
                accession_sign_plus.append(None)
                sign_minus.append(None)
                accession_sign_minus.append(None)
        else:
            sign_plus.append(None)
            accession_sign_plus.append(None)
            sign_minus.append(None)
            accession_sign_minus.append(None)

    # Create a DataFrame to save the significant points and their annotations
    significant_df = pd.DataFrame({
        'Significant_Overexpressed': sign_plus,
        'Accession Number +': accession_sign_plus,
        'Significant_Underexpressed': sign_minus,
        'Accession Number -': accession_sign_minus
    })

    # Drop rows with all None values
    significant_df.dropna(how='all', inplace=True)

    # Write the DataFrame to a file
    output_filename = os.path.join(output_path, f"{title}_significant.csv")
    significant_df.to_csv(output_filename, sep='\t', index=False)

    return significant_df

if __name__ == "__main__": 
    if len(sys.argv) != 3:  # Check if there are exactly 2 arguments
        print("Usage: python significant.py </path/input_filename> </path/output_folder/>")
        sys.exit(1)
    
    inputfile = sys.argv[1]
    output_folder = sys.argv[2]

    # Load the input file into a DataFrame
    df = pd.read_csv(inputfile, sep='\t')

    # Extract the relevant columns
    log2_fold_change = df.iloc[:, 23]
    transformed_pvalues = df.iloc[:, 24]
    annotations = df.iloc[:, 1] 
    accessions = df.iloc[:, 2]

    title = os.path.basename(inputfile).replace(".txt", "")
    
    significant_list(title, log2_fold_change=log2_fold_change, transformed_pvalues=transformed_pvalues, annotations=annotations, accessions=accessions output_path=output_folder)