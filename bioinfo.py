#!/usr/bin/env python
# Author: <Bailey Knight> <baileyknight3@gmail.com>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.4"         # v0.4 includes all functions needed for module submission.
                            # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = set('ATCGNactgn')
RNA_bases = set('AUCGNaucgn')

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter)-33

def qual_score(phred_score: str) -> float:
    '''This function should calculate the average quality 
       score of the whole phred string.
    '''
    total: int = 0
    for score in phred_score:
       total += convert_phred(score)
    return total/len(phred_score)

def validate_base_seq(seq: str, RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    return set(seq)<=(RNA_bases if RNAflag else DNA_bases)

#leslie gave this one that was not full of bases
def gc_content(seq: str):
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(seq), "String contains invalid characters - are you sure you used a DNA sequence?"
    seq = seq.upper()
    return (seq.count('G') + seq.count('C'))/ len(seq)


def calc_median(list):
    '''Takes list as input and finds returns the value at the median index.
       First,returns half length of list 
       Then if list is even length take the average of the 2 middle values. otherwise take median value at integer.'''
    half_length: int=(len(list)-1)//2

    if len(list) %2==0:
        median = (list[half_length] + list[half_length+1]) / 2
    else:
        median = list[half_length]
    return median

def oneline_fasta(fileread, filewrite):
    '''This takes a multiline fasta file and returns a fasta file that is 2 lines
        1 line is header and 1 line is sequence.'''
    with open(filewrite, 'w') as fhw:
        with open(fileread, 'r') as fhr:
            firstline = True
            aaseq = ''
            for line in fhr:
                if firstline == True:
                    fhw.write(line)
                    firstline = False
                if line.startswith('>'):
                    fhw.write(aaseq)
                    fhw.write('\n')
                    fhw.write(line)
                    aaseq = ''
                else:
                    aaseq += line.strip()
            fhw.write(aaseq)

if __name__ == "__main__":
    # tests for convert_phred (These tests were provided by Leslie Coonrod)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")
    
    # tests for qual_score
    print(qual_score("ABCDE"))
    assert qual_score("ABCDE")== 34,  "wrong answer"
    assert qual_score("EFGH") == 37.5,  "wrong answer"
    print("your qscore function works")
    
    # tests for validate_base_seq
    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("Hi there!") == False, "Validate base seq fails to recognize nonDNA"
    assert validate_base_seq("Hi there!", True) == False, "Validate base seq fails to recognize nonDNA"
    print("Passed DNA and RNA tests")
    
    # test for gc_content function
    assert gc_content('ACTG') == 0.5, "correct answer"
    assert gc_content('ACTG') != 1, "correct answer"
    assert gc_content('ACTGCCCCCCCCCG') == 0.8571428571428571, "correct answer"
    print("passed GC content test")
    
    #test for median calc
    assert calc_median([1, 2, 3]) == 2, "correct answer"
    assert calc_median([1, 2, 3, 4]) == 2.5, "correct answer"
    assert calc_median([500, 700, 800, 900, 1000, 1000, 2000, 3000]) == 950, "correct answer"
    print("passed median calc test")
    
    
    #end tests
    print("one_line fasta not tested and not needed per leslie")
    print('passed all test')
