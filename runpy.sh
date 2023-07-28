#!/bin/bash                                  
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --cpus-per-task=4                 #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4GB may need to change stuff


#example run sbatch ./runpy.sh TEST-input_FASTQ/unit_testR1.fq 
set -e

filename=$1
length_read=$(zcat $filename | head -2 | grep -v "^@" | wc -L)
#test with test file
#length_read=$(cat $filename | head -2 | wc -L)


conda activate demultiplex

echo "read length = $length_read"
echo "start python script"
/usr/bin/time -v \
    ./mean_qscore.py -f "$filename" -l $length_read

conda deactivate