#!/bin/bash

# This script is to run statistics.py file on all files with all files in a specific directory. 
# usage: bash run_statistics.sh ˜/INPUT/DIRECTORY/

directory="$1"

for file1 in "$directory/*annotated.txt"
do
	for file2 in "$directory/*annotated.txt"
	do 
		python /Users/fadimestemmer/Desktop/Saito_Lab/Bioinformatics/LCMS_Proteomics_Data_Evaluation/statistics.py "$file1" "$file2"
	done
done

