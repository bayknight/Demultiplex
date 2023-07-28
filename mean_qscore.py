#!/usr/bin/env python

#Bailey Knight 27 July 2023
'''The purpose of this is to get mean quality score and plot it on a histogram. see runpy.sh for argument input 
    and example of run command.'''



import bioinfo
import argparse
import gzip
from matplotlib import pyplot as plt


def get_args():
    '''argument parser for generating input in terminal. All arguments are necessary
        -f input File name
        -l length of read
        -k kmer size
        -o output file name'''
    parser = argparse.ArgumentParser(description="A program to introduce yourself")
    parser.add_argument("-f", "--filename", help="Your filename", type=str)
    parser.add_argument("-l", "--lengthread", help="read_length", type=int)
    return parser.parse_args()



def init_list(lst: list, list_length: int, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    lst = [value]*list_length
    return lst


def populate_list(file: str, list_length) -> 'tuple[list, int]':
    """populate list with sums of basepairs
        changed to return number of read lines
       added gzip to this size files are .gz"""
    my_list: list = []
    my_list = init_list(my_list, list_length)
    num_lines= 0
    i=0
    with gzip.open(file, 'rt') as fh:
        for line in fh:
            line = line.strip()
            if i%4 == 3:
                phred_total=0
                j=0
                num_lines+=1
                for char in line:
                    phred_total=bioinfo.convert_phred(char)
                    my_list[j] += phred_total
                    j+=1
        
            i+=1                 
    return my_list, num_lines



def calc_mean_phreds(my_list, num_lines):
    for i, value in enumerate(my_list):
        my_list[i]= value/(num_lines)
    return my_list




if __name__ == '__main__':

    #calling argparser
    args = get_args()

    #set variables
    filename = args.filename
    length_read  = args.lengthread


    my_list, num_lines =  populate_list(filename, length_read)
    print(my_list)
    #calculate means
    calc_mean_phreds(my_list, num_lines)
    print(my_list)
    filename = filename.split('/')[-1]
    
    plt.bar(range(len(my_list)),my_list, color='c')
    plt.xlabel("Base Position")
    plt.ylabel("Mean Quality Score")
    plt.title("Mean Quality Scores")
    plt.savefig(f'{filename}_hist.png')
    
    
