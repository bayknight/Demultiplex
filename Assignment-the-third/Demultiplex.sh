#!/bin/bash                                  
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --cpus-per-task=4                 #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4GB may need to change stuff


#example run sbatch  ./Demultiplex.sh /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz /projects/bgmp/shared/2017_sequencing/indexes.txt

file_1=$1
file_2=$2
file_3=$3
file_4=$4
dict_file=$5

conda activate demultiplex
echo "start run"

/usr/bin/time -v \
    ./Demultiplex.py -f1 "$file_1" -f2 "$file_2" -f3 "$file_3" -f4 "$file_4" -d "$dict_file"




conda deactivate

exit
