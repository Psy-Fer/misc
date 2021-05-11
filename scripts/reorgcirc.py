import os
import sys
import argparse
import edlib
'''

    James M. Ferguson (j.ferguson@garvan.org.au)
    Genomic Technologies
    Garvan Institute
    Copyright 2021

    script description

    install edlib library to python3
	> pip3 install edlib

	This will align the -s sequence against each circular sequence in the fasta file
	It will then print out the new re-organised sequence, starting with the start site of the alignment,
	adding the original start of the assembly to the end.

	run like this:
	python3 reorgcirc.py -f assembly.fasta -s ATCGGCTGATTGCTAGCTTGATCGA -m 3 > new.fasta

	This will search for the BEST score with a maximum edit distance of 3 in the alignment.

    Currently breaks if the fasta is split on new lines ever 80 characters.
    Will fix soon

    ----------------------------------------------------------------------------
    version 0.0 - initial



    TODO:
        -

    ----------------------------------------------------------------------------
    MIT License

    Copyright (c) 2021 James Ferguson

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    '''
    do the thing
    '''
    parser = MyParser(
        description="re-organise circular assembly given query sequence as new start")
    #group = parser.add_mutually_exclusive_group()
    parser.add_argument("-f", "--fasta",
                        help="fasta file with assemblies")
    parser.add_argument("-s", "--sequence",
                        help="base sequence to search for")
    parser.add_argument("-m", "--missmatch", type=int,
                        help="Number of allowed missmatches for sequence. 0=exact")

    args = parser.parse_args()

    # print help if no arguments given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    q = args.sequence.lower()

    with open(args.fasta, 'r') as f:
        for l in f:
            l = l.strip('\n')
            if l[0] == ">":
                name = l
            else:
                seq = l
                k = edlib.align(q, l.lower(),
                                mode="HW", task="locations", k=args.missmatch)
                if k['locations']:
                    start = k['locations'][0][0]
                    end = k['locations'][0][1]
                    score = k['editDistance']
                    print("{} start={} end={} score={}".format(name, start, end, score))
                    print(l[start:]+l[:start])

if __name__ == '__main__':
    main()
