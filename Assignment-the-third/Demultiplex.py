#!/usr/bin/env python

#Bailey Knight 8 July
''''''


import argparse
import itertools
import gzip


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

    #get 4 files + index file
    file_1 = args.file1
    file_2 = args.file2
    file_3 = args.file3
    file_4 = args.file4
    dict_file = args.dictfile

    #make the index from the file into a set
    index_set = set()
    with open(dict_file, 'r') as dfh:
        dfh.readline()
        for line in dfh:
            line = line.split()
            index_set.add(line[4])
    
    #generate all combinations of index pairs
    pair_set = set(itertools.combinations(index_set, 2))
    #make empty hopped dictionary and matched dictionary
    

    #open all file handles and make list of them to close later
    fhandles = {}
    for index in index_set:   
        R1 = open(f'{index}_R1.fq', 'w')
        R2 = open(f'{index}_R2.fq', 'w')
        fhandles[index]= (R1,R2)
    U1 = open('Unknown_R1.fq', 'w')
    U2 = open('Unknown_R2.fq', 'w')
    H1 = open('Hopped_R1.fq', 'w')
    H2 = open('Hopped_R2.fq', 'w')
    

    hopped_dict = {}
    matched_dict = {}
    unknown_dict = {}
    #iterate through the 4 input fastq files
    with gzip.open(file_1, 'rt') as r1, gzip.open(file_2, 'rt') as r2, gzip.open(file_3, 'rt') as r3, gzip.open(file_4, 'rt') as r4:
        
        total=0
        while True:
            #generate lists to hold record lines
            r1_list, r2_list, r3_list, r4_list =[], [], [], []
            
            r1_line1 =r1.readline().strip()
            r2_line1 =r2.readline().strip()
            r3_line1 =r3.readline().strip()
            r4_line1 =r4.readline().strip()
            if r1_line1 == '':
                break
            
            r1_list.append(r1_line1)
            r2_list.append(r2_line1)
            r3_list.append(r3_line1)
            r4_list.append(r3_line1)
            
            r1_list.append(r1.readline().strip())
            r2_list.append(r2.readline().strip())
            r3_list.append(r3.readline().strip())
            r4_list.append(r4.readline().strip())

            r1_list.append(r1.readline().strip())
            r2_list.append(r2.readline().strip())
            r3_list.append(r3.readline().strip())
            r4_list.append(r4.readline().strip())

            r1_list.append(r1.readline().strip())
            r2_list.append(r2.readline().strip())
            r3_list.append(r3.readline().strip())
            r4_list.append(r4.readline().strip())

            #print(r1_list)
            #print(r2_list)
            #print(r3_list)
            #print(r4_list)
            index = r2_list[1]
            reverse_comp = rev_comp(r3_list[1])
            #add in qscore filtering if needed right here

            if index not in index_set or reverse_comp not in index_set:
                U1.write(f'{r1_list[0]} {index}:{reverse_comp}\n{r1_list[1]}\n{r1_list[2]}\n{r1_list[3]}\n')
                U2.write(f'{r4_list[0]} {index}:{reverse_comp}\n{r4_list[1]}\n{r4_list[2]}\n{r4_list[3]}\n')
                key = (index, reverse_comp)
                if key in unknown_dict:
                    unknown_dict[key]+=1
                else:
                    unknown_dict[key]=1
            
            elif index == reverse_comp:
                fhandles[index][0].write(f'{r1_list[0]} {index}:{reverse_comp}\n{r1_list[1]}\n{r1_list[2]}\n{r1_list[3]}\n')
                fhandles[index][1].write(f'{r4_list[0]} {index}:{reverse_comp}\n{r4_list[1]}\n{r4_list[2]}\n{r4_list[3]}\n')
                if index in matched_dict:
                    matched_dict[index]+=1
                else:
                    matched_dict[index]=1
            
            elif index != reverse_comp:
                H1.write(f'{r1_list[0]} {index}:{reverse_comp}\n{r1_list[1]}\n{r1_list[2]}\n{r1_list[3]}\n')
                H2.write(f'{r4_list[0]} {index}:{reverse_comp}\n{r4_list[1]}\n{r4_list[2]}\n{r4_list[3]}\n')
                key = (index, reverse_comp)
                if key in hopped_dict:
                    hopped_dict[key]+=1
                else:
                    hopped_dict[key]=1
            
            total+=1
            
                
    for key in fhandles:
        fhandles[key][0].close()
        fhandles[key][1].close()

    matched_pairs = sum(matched_dict.values())
    unknown_pairs = sum(unknown_dict.values())
    hopped_pairs = sum(hopped_dict.values())
    percent_matched = matched_pairs/total*100
    percent_unknown = unknown_pairs/total*100
    percent_hopped = hopped_pairs /total*100
   
    
    index_total_freq = {}
    hopped_total_freq = {}
    for key in matched_dict:
        index_total_freq[key] = (matched_dict[key], (matched_dict[key]/matched_pairs*100), (matched_dict[key]/total*100))
    
    for key in hopped_dict:
        hopped_total_freq[key] = (hopped_dict[key], (hopped_dict[key]/hopped_pairs*100), (hopped_dict[key]/total*100))



    with open('report_demultiplex.md', 'w') as fhw:
        fhw.write(f'Run Report<br>Files Used to Generate Report:<br>{file_1}<br>{file_2}<br>{file_3}<br>{file_4}<br>')
        fhw.write('Run Summary:\n```\n')
        fhw.write(f'Total Read Pairs: {total} (100%)\nMatched Index Pairs: {matched_pairs} ({percent_matched}%)\nHopped Index Pairs: {hopped_pairs} ({percent_hopped}%)\nUnknown Index Pairs: {unknown_pairs} ({percent_unknown}%)\n')
        fhw.write('```\n')
        fhw.write('\n| Index Pairs | Frequency | Percent of Matched Pairs | Percent Matched Pairs of Total Reads |  \n')
        fhw.write('|---|---|---|---|  \n')
        for key in index_total_freq:
            fhw.write(f'|{key}|{index_total_freq[key][0]}|{index_total_freq[key][1]}|{index_total_freq[key][2]}|  \n')
        fhw.write('\n\n\n')
        fhw.write('| Hopped Index Pairs | Frequency | Percent of Total Hopped Pairs | Percent Index Hops of Total Reads |  \n')
        fhw.write('|---|---|---|---|  \n')
        for key in hopped_total_freq:
            fhw.write(f'|{key}|{hopped_total_freq[key][0]}|{hopped_total_freq[key][1]}|{hopped_total_freq[key][2]}|  \n')