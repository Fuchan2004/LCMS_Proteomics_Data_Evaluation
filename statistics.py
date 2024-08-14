#!/usr/bin/env python3

'''
This script is used to generate statistics important for creating xy-plots and volcanoplots of proteome data. Make sure that all files are in the correct format (see README.md) and that all annotations are present. This script has several steps: 
    1. Normalize the results 
    2. Calcualte mean counts for each measurement
    3. Determine the standard deviation of each measurement
    4. Create a new file for each treatment comparison with the combined data
    5. Determine log2fold changes
    6. Calculate p-values

USAGE: python statistics.py </path/input_filename_1> </path/output_filename/>
'''

import glob
import os
import sys


def normalization(file_1, file_2):    
    filename_1 = os.path.basename(file_1)  # Get the filename
    filename_2 = os.path.basename(file_2)  # Get the filename
    print(f"Normalizing values in file: {filename_1, filename_2}")

    # Read the original files
    with open(file_1, 'r') as file_1:
        lines_1 = file_1.readlines()
    with open(file_2, 'r') as file_2:
        lines_2 = file_2.readlines()

    for line_1 in lines_1[1:]:
        columns_1 = line_1.strip().split('\t')
        for line_2 in lines_2[1:]:
            columns_2 = line_2.strip.split('\t')
        
            SC1 = columns_1['1'].sum()
            SC2 = columns_1['2'].sum()
            SC3 = columns_1['3'].sum()
            SC4 = columns_2['1'].sum()
            SC5 = columns_2['2'].sum()
            SC6 = columns_2['3'].sum()
    
            # Calculate the average of the sums
            sum_SC = SC1 + SC2 + SC3 + SC4 + SC5 + SC6
            avg_SC = sum_SC / 6
    
            # Normalize each row 
            columns_1['norms_1'] = (columns_1['1'] / SC1) * avg_SC
            columns_1['norms_2'] = (columns_1['2'] / SC2) * avg_SC
            columns_1['norms_3'] = (columns_1['3'] / SC3) * avg_SC
            columns_2['norms_1'] = (columns_2['1'] / SC4) * avg_SC
            columns_2['norms_2'] = (columns_2['2'] / SC5) * avg_SC
            columns_2['norms_3'] = (columns_2['3'] / SC6) * avg_SC
    
    # Write the normalized lines back to a new file
    strain = filename_1.split('_')[1]
    medium_1 = filename_1.split('_')[2]
    medium_2 = filename_2.split('_')[2]
    phase_1 = filename_1.split('_')[3]
    phase_2 = filename_2.split('_')[3]
    
    output_filename = 'strain' + 'medium_1' + 'medium_2' + 'phase_1' + 'phase_2' + '.txt'
        
    with open(output_filename, 'w') as file:
        file.writelines()
        
        print(f"Normalized data written to: {output_filename}")

# Computing the row-wise average + standard deviation 
def statistics(df):
    row_wise_average = df.mean(axis=1)
    standard_deviation = df.std(axis=1)
    df['Row_Average']= row_wise_average
    df['STD'] = standard_deviation

def merge_and_format(df1, df2, suf_1='', suf_2=''):
    merged_df = pd.merge(df1, df2, on="Accession Number", how="outer", suffixes=(suf_1, suf_2))
    merged_df.fillna(0, inplace=True)
    merged_df['Annotation{}'.format(suf_1)] = merged_df['Annotation{}'.format(suf_1)].replace(0, "Unknown")
    merged_df['Annotation{}'.format(suf_2)] = merged_df['Annotation{}'.format(suf_2)].replace(0, "Unknown")
    return merged_df

def calculate_log2(df1, df2):
    log2 = np.log2(df1.div(df2))
    log2.fillna(0, inplace=True)
    return log2

# df1 and df2 are the dataframes containing the values of the triplicate measurements of treatment 1 and 2 respectively
def calculate_pvalue(df1, df2):
    num_values= df1.shape[0] # identifies the number of rows
    p_values = []

    print(num_values, df1.shape, df2.shape)
    
    for row in range(num_values):
        #This line performs a two-sample t-test for the current row of data. df1.iloc[row].values and df2.iloc[row].values select the values of the current row from df1 and df2, respectively. These are passed as arguments to stats.ttest_ind, which computes the t-test for the means of two independent samples. The result is stored in the variable ttest_result.
        ttest_result = stats.ttest_ind(df1.iloc[row].values, df2.iloc[row].values)
        p_values.append(ttest_result.pvalue)
        transformed_pvals = -1*np.log10(num_values*np.array(p_values))
    return transformed_pvals

def format_pval_df(pval):
    pval_df = pd.DataFrame(pval, columns=["tpv"])
    pval_df.fillna(0, inplace=True)
    # Extract as variable
    transformed_pval = pval_df["tpv"]
    return transformed_pval

if __name__ == "__main__": 
    
    if len(sys.argv) !=2: # If there is more than 1 argument to call this script, it will provide guidance on how to use it.
        print("Usage: python format_proteomefile.py <input_foldername>")
        sys.exit(1)
    
    folder = sys.argv[1]
    format_proteomefiles(folder)