#!/usr/bin/env python3

'''
This script contains a FUNCTION TO PLOT TRANSFORMED p-values FROM A STUDENT T-TEST AGAINST log2FOLD CHANGES (FROM TRIPLICATE MEASUREMENTS) OF TWO DATASETS AS VOLCANO PLOT. The datasets need to be in the same input file. Therefore, the input file must be generated from a combination of following steps (in order): 
    1. format_proteomefile.py
    2. annotate.py (Only if annotations were missing in the original file)
    3. statistics.py

The input file needs to have 25 columns, where the extension '_1' is condition 1, and '_2' is condition 2: 
#_1	Annotation_1	Accession Number	1_1	2_1	3_1	Control_1	norms_1_1	norms_2_1	norms_3_1	#_2	Annotation_2	1_2	2_2	3_2	Control_2	norms_1_2	norms_2_2	norms_3_2	Row_Average_1	STD_1	Row_Average_2	STD_2	Log2_Fold_Change	Transformed_P_Value


title = Title of the plot
x_axis_title = "log2 fold change"
y_axis_title = "-log10 pvalue"
point_radius = 4, can be changed but 4 works well
log2_fold_change = log2 fold change calculated from statistics.py function and saved in Log2_Fold_Change dataframe
transformed_pvalues = p-value calculated from statistics.py function and saved in Transformed_P_Value dataframe
annotations = annotations for the respective log2fold change and p-values. 
output_path = filepath where output figures should be saved.

USAGE: python xy_plot.py </path/input_filename.txt> </path/output_foldername/>
'''

import os
import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

def volcano_plot(title, log2_fold_change, transformed_pvalues, annotations, output_path, x_axis_title="log2 fold change", y_axis_title="-log10 pvalue", point_radius=4):

    fig = go.Figure()
    fig.update_layout(
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    colors = []

    for i in range(len(log2_fold_change)):
        if transformed_pvalues[i] > 2:
            if log2_fold_change[i] > 0.5:
                colors.append('#db3232')
            elif log2_fold_change[i] < -0.5:
                colors.append('#3f65d4')
            else:
                colors.append('rgba(150,150,150,0.5)')
        else:
            colors.append('rgba(150,150,150,0.5)')

    fig.add_trace(
        go.Scattergl(
            x=log2_fold_change,
            y=transformed_pvalues,
            mode='markers',
            text=annotations,
            hovertemplate='%{text}: %{x}<br>',
            marker={
                'color': colors,
                'size': point_radius,
            }
        )
    )
    
    # Save the plot as an HTML file
    output_html = os.path.join(output_path, f"volcano_{title}.html")
    plot(fig, filename=output_html)

    # Save the plot as a PDF file
    output_pdf = os.path.join(output_path, f"volcano_{title}.pdf")
    fig.write_image(output_pdf)

if __name__ == "__main__": 
    if len(sys.argv) != 3:  # Check if there are exactly 2 arguments
        print("Usage: python volcano_plot.py </path/input_filename.txt> </path/output_foldername/>")
        sys.exit(1)
    
    inputfile = sys.argv[1]
    output_folder = sys.argv[2]

    # Load the input file into a DataFrame
    df = pd.read_csv(inputfile, sep='\t')

    # Extract the relevant columns
    log2_fold_change = df.iloc[:, 23]
    transformed_pvalues = df.iloc[:, 24]
    annotations = df.iloc[:, 1] 

    title = os.path.basename(inputfile).replace(".txt", "")
    
    volcano_plot(title, log2_fold_change=log2_fold_change, transformed_pvalues=transformed_pvalues, annotations=annotations, output_path=output_folder)