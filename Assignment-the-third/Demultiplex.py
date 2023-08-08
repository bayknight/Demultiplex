#!/usr/bin/env python

#Bailey Knight 8 July
''''''


import argparse
import itertools


def get_args():
    '''argument parser for generating input in terminal. All arguments are necessary
        -f input File name
        -d length of read
        '''
    parser = argparse.ArgumentParser(description="A program to introduce yourself")
    parser.add_argument("-f1", "--file1", help="Your filename", type=str)
    parser.add_argument("-f2", "--file2", help="Your filename", type=str)
    parser.add_argument("-f3", "--file3", help="Your filename", type=str)
    parser.add_argument("-f4", "--file4", help="Your filename", type=str)
    parser.add_argument("-d", "--dictfile", help="dict_file", type=str)
    return parser.parse_args()

nt_dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C', 'N':'N'}

def rev_comp(seq: str):
    seq = seq[::-1]
    reverse_comp = ''
    for char in seq:
        if char in nt_dict:
            reverse_comp += nt_dict[char]
    return reverse_comp

if __name__ == '__main__':
    
    #get argparse
    args = get_args()

    file_1 = args.file1
    file_2 = args.file2
    file_3 = args.file3
    file_4 = args.file4
    dict_file = args.dictfile

    index_set = set()
    with open(dict_file, 'r') as dfh:
        dfh.readline()
        for line in dfh:
            line = line.split()
            index_set.add(line[4])
    

    pair_set = set(itertools.combinations(index_set, 2))

    for value in index_set:   
        R1= open (f'{value}_R1.fastq', 'w')
        R2= open(f'{value}_R2.fastq', 'w')
        R1.close
        R2.close
        

            
