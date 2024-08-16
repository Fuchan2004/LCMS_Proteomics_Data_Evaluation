#!/usr/bin/env python3

'''
This script contains a FUNCTION TO PLOT AVERAGED AND NORMALIZED SPECTRAL COUNTS (FROM TRIPLICATE MEASUREMENTS) OF TWO DATASETS AS X-Y-PLOT. The datasets need to be in the same input file. Therefore, the input file must be generated from a combination of following steps (in order): 
    1. format_proteomefile.py
    2. annotate.py (Only if annotations were missing in the original file)
    3. statistics.py

The input file needs to have 25 columns, where the extension '_1' is condition 1, and '_2' is condition 2: 
#_1	Annotation_1	Accession Number	1_1	2_1	3_1	Control_1	norms_1_1	norms_2_1	norms_3_1	#_2	Annotation_2	1_2	2_2	3_2	Control_2	norms_1_2	norms_2_2	norms_3_2	Row_Average_1	STD_1	Row_Average_2	STD_2	Log2_Fold_Change	Transformed_P_Value

df1: dataframe containing normalized spectral counts of condition 1
df2: dataframe containing normalized spectral counts of condition 2
df3: dataframe containing Annotations
df4: dataframe containing standard deviation of condition 1
df5: dataframe containing standard deviation of condition 2
title = Title of the plot
filename = filename of .html/.pdf file generated
width = width of plot
height = height of plot


USAGE: python xy_plot.py </path/input_filename.txt> </path/output_foldername/>
'''

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
from plotly.offline import plot

def plot_and_regression(df1, df2, df3, df4, df5, title, output_path, width=1000, height=1000):
    x = df1.values
    y = df2.values
    z = df3.values
    yerr = df4.values
    xerr = df5.values
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Calculate predicted values
    predicted_values = slope * x + intercept
    
    # Calculate R squared
    r_squared = r_value ** 2

    # Filter data points based on annotation
    protease_indices = df1.index[df3.str.contains('protease', case=False)]
    peptidase_indices = df1.index[df3.str.contains('peptidase', case=False)]
    metalloprotease_indices = df1.index[df3.str.contains('metalloprotease', case=False)]
    metallopeptidase_indices = df1.index[df3.str.contains('metallopeptidase', case=False)]
    non_protease_indices = df1.index[~df3.str.contains('protease|peptidase|metalloprotease|metallopeptidase', case=False)]

    # Create traces for each category
    trace_non_protease = go.Scatter(
        x=x[non_protease_indices],
        y=y[non_protease_indices],
        error_y=dict(type='data', array=yerr[non_protease_indices]),
        error_x=dict(type='data', array=xerr[non_protease_indices]),
        mode='markers',
        name='Non-Protease',
        text=z[non_protease_indices],
        marker=dict(color='black')
    )

    trace_protease = go.Scatter(
        x=x[protease_indices],
        y=y[protease_indices],
        error_y=dict(type='data', array=yerr[protease_indices]),
        error_x=dict(type='data', array=xerr[protease_indices]),
        mode='markers',
        name='Protease',
        text=z[protease_indices],
        marker=dict(color='blue')
    )

    trace_peptidase = go.Scatter(
        x=x[peptidase_indices],
        y=y[peptidase_indices],
        error_y=dict(type='data', array=yerr[peptidase_indices]),
        error_x=dict(type='data', array=xerr[peptidase_indices]),
        mode='markers',
        name='Peptidase',
        text=z[peptidase_indices],
        marker=dict(color='red')
    )

    trace_metallopeptidase = go.Scatter(
        x=x[metallopeptidase_indices],
        y=y[metallopeptidase_indices],
        error_y=dict(type='data', array=yerr[metallopeptidase_indices]),
        error_x=dict(type='data', array=xerr[metallopeptidase_indices]),
        mode='markers',
        name='Metallopeptidase',
        text=z[metallopeptidase_indices],
        marker=dict(color='pink')
    )

    trace_metalloprotease = go.Scatter(
        x=x[metalloprotease_indices],
        y=y[metalloprotease_indices],
        error_y=dict(type='data', array=yerr[metalloprotease_indices]),
        error_x=dict(type='data', array=xerr[metalloprotease_indices]),
        mode='markers',
        name='Metalloprotease',
        text=z[metalloprotease_indices],
        marker=dict(color='lightblue')
    )

    # Linear regression line
    trace_regression = go.Scatter(
        x=x,
        y=predicted_values,
        mode='lines',
        name='Linear Regression',
        line=dict(color='red')
    )

    data = [trace_non_protease, trace_protease, trace_peptidase, trace_metallopeptidase, trace_metalloprotease, trace_regression]

    layout = go.Layout(
        title=f'{title} (R² = {r_squared:.2f})',
        xaxis=dict(title=df1.name),
        yaxis=dict(title=df2.name),
        showlegend=True,
        width=width,
        height=height
    )
    fig = go.Figure(data=data, layout=layout)

    # Save the plot as an HTML file
    output_html = os.path.join(output_path, f"{title}.html")
    plot(fig, filename=output_html)

    # Save the plot as a PDF file
    output_pdf = os.path.join(output_path, f"{title}.pdf")
    fig.write_image(output_pdf)

    return slope, intercept, std_err, df1, df2, df3

if __name__ == "__main__": 
    if len(sys.argv) != 3:  # Check if there are exactly 2 arguments
        print("Usage: python xy_plot.py </path/input_filename.txt> </path/output_foldername/>")
        sys.exit(1)
    
    inputfile = sys.argv[1]
    output_folder = sys.argv[2]

    # Load the input file into a DataFrame
    df = pd.read_csv(inputfile, sep='\t')

    # Extract the relevant columns
    df1 = df.iloc[:, 19]
    df2 = df.iloc[:, 21]
    df3 = df.iloc[:, 1] 
    df4 = df.iloc[:, 20]
    df5 = df.iloc[:, 22]

    title = os.path.basename(inputfile).replace(".txt", "")
    
    plot_and_regression(df1, df2, df3, df4, df5, title, output_folder)
