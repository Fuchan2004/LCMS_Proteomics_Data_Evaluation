#!/usr/bin/env python3

'''
This script is used to generate statistics important for creating xy-plots and volcanoplots of proteome data. Make sure that all files are in the correct format (see README.md) and that all annotations are present. This script has several steps: 
    1. Normalize the results 
    2. Calcualte mean counts for each measurement
    3. Determine the standard deviation of each measurement
    4. Create a new file for each treatment comparison with the combined data
    5. Determine log2fold changes
    6. Calculate p-values

USAGE: python statistics.py </path/input_filename_1> </path/input_filename_2/>
'''

import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats

def merge_and_format(df1, df2, suf_1='', suf_2=''):
    # Merge the dataframes based on "Accession Number"
    merged_df = pd.merge(df1, df2, on="Accession Number", how="outer", suffixes=(suf_1, suf_2))
    
    # Fill missing values with 0
    merged_df.fillna(0, inplace=True)
    
    # Replace 0 in annotations with "Unknown"
    merged_df[f'Annotation{suf_1}'] = merged_df[f'Annotation{suf_1}'].replace(0, "Unknown")
    merged_df[f'Annotation{suf_2}'] = merged_df[f'Annotation{suf_2}'].replace(0, "Unknown")
    
    return merged_df

def calculate_log2(df1, df2):
    log2 = np.log2(df1.div(df2))
    log2.fillna(0, inplace=True)
    return log2

def calculate_pvalue(df1, df2):
    num_values = df1.shape[0]
    p_values = []
    
    for row in range(num_values):
        ttest_result = stats.ttest_ind(df1.iloc[row].values, df2.iloc[row].values)
        p_values.append(ttest_result.pvalue)
    
    transformed_pvals = -1 * np.log10(num_values * np.array(p_values))
    return transformed_pvals

def normalization(file_1, file_2):    
    filename_1 = os.path.basename(file_1)
    filename_2 = os.path.basename(file_2)
    print(f"Normalizing values in files: {filename_1}, {filename_2}")

    # assign variables for the conditions
    strain = filename_1.split('_')[1]
    medium_1 = filename_1.split('_')[2]
    medium_2 = filename_2.split('_')[2]
    phase_1 = filename_1.split('_')[3]
    phase_2 = filename_2.split('_')[3]

    if medium_1 == medium_2: 
        suf_1 = phase_1
        suf_2 = phase_2
    elif phase_1 == phase_2:
        suf_1 = medium_1
        suf_2 = medium_2

    # Read files into pandas dataframes
    df1 = pd.read_csv(file_1, sep='\t')
    df2 = pd.read_csv(file_2, sep='\t')

    # Convert the columns to numeric, coercing any errors to NaN
    df1.iloc[:, 3:6] = df1.iloc[:, 3:6].apply(pd.to_numeric, errors='coerce')
    df2.iloc[:, 3:6] = df2.iloc[:, 3:6].apply(pd.to_numeric, errors='coerce')

    # Calculate sums for the columns
    SC1, SC2, SC3 = df1.iloc[:, 3:6].sum()
    SC4, SC5, SC6 = df2.iloc[:, 3:6].sum()

    # Calculate the average of the sums
    sum_SC = SC1 + SC2 + SC3 + SC4 + SC5 + SC6
    avg_SC = sum_SC / 6

    # Normalize the data
    df1[f'norms_1_{suf_1}'] = (df1.iloc[:, 3] / SC1) * avg_SC
    df1[f'norms_2_{suf_1}'] = (df1.iloc[:, 4] / SC2) * avg_SC
    df1[f'norms_3_{suf_1}'] = (df1.iloc[:, 5] / SC3) * avg_SC

    df2[f'norms_1_{suf_2}'] = (df2.iloc[:, 3] / SC4) * avg_SC
    df2[f'norms_2_{suf_2}'] = (df2.iloc[:, 4] / SC5) * avg_SC
    df2[f'norms_3_{suf_2}'] = (df2.iloc[:, 5] / SC6) * avg_SC

    # Merge and format the dataframes
    combined_df = merge_and_format(df1, df2, suf_1, suf_2)

    # Calculate row-wise averages and standard deviations for normalized columns
    combined_df[f'Row_Average_{suf_1}'] = combined_df[[f'norms_1_{suf_1}', f'norms_2_{suf_1}', f'norms_3_{suf_1}']].mean(axis=1)
    combined_df[f'STD_{suf_1}'] = combined_df[[f'norms_1_{suf_1}', f'norms_2_{suf_1}', f'norms_3_{suf_1}']].std(axis=1)

    combined_df[f'Row_Average_{suf_2}'] = combined_df[[f'norms_1_{suf_2}', f'norms_2_{suf_2}', f'norms_3_{suf_2}']].mean(axis=1)
    combined_df[f'STD_{suf_2}'] = combined_df[[f'norms_1_{suf_2}', f'norms_2_{suf_2}', f'norms_3_{suf_2}']].std(axis=1)

    # Add log2 fold change and p-values to your combined_df
    log2_df = calculate_log2(combined_df[f'Row_Average_{suf_1}'], combined_df[f'Row_Average_{suf_2}'])
    pval_df = calculate_pvalue(combined_df[[f'norms_1_{suf_1}', f'norms_2_{suf_1}', f'norms_3_{suf_1}']],
                           combined_df[[f'norms_1_{suf_2}', f'norms_2_{suf_2}', f'norms_3_{suf_2}']])

    combined_df['Log2_Fold_Change'] = log2_df
    combined_df['Transformed_P_Value'] = pval_df

    # Get the directory of the input files
    input_directory = os.path.dirname(file_1)

    # Create the output file path using the same directory
    if medium_1 == medium_2: 
        output_filename = os.path.join(input_directory, f'{strain}_{medium_1}_{phase_1}VS{phase_2}.txt')
    elif phase_1 == phase_2: 
        output_filename = os.path.join(input_directory, f'{strain}_{phase_1}_{medium_1}VS{medium_2}.txt')
    
    combined_df.to_csv(output_filename, sep='\t', index=False)

    print(f"Log2 fold change and p-values added. Data written to: {output_filename}")

if __name__ == "__main__": 
    if len(sys.argv) != 3:
        print("Usage: python statistics.py <input_filename_1> <input_filename_2>")
    else:
        normalization(sys.argv[1], sys.argv[2])