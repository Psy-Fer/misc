import os
import sys
import argparse
# import edlib
import mappy as mp
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
    parser.add_argument("-r", "--ref",
                        help="fasta with sequences to search for")
    parser.add_argument("-m", "--missmatch", type=int, default=10,
                        help="Number of allowed missmatches for sequence. 0=exact")

    args = parser.parse_args()

    # print help if no arguments given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # q = args.sequence.lower()
    #
    # a = mp.Aligner(args.ref, preset="splice")

    baits = {}
    with open(args.ref, 'r') as f:
        for l in f:
            l = l.strip('\n')
            if l[0] == ">":
                name = l
            else:
                seq = l
                baits[name] = seq


    # might need to do this twice, second time with seq = seq[len/2:]+seq[:len/2] to get end hits
    map_dic = {}
    C = 0
    a = mp.Aligner(args.fasta, preset="map-ont")
    if not a:
        raise Exception("ERROR: failed to load/build index")
    C = 0
    for bait in baits:
        # print(bait)
        # print(baits[bait])
        for hit in a.map(baits[bait]): # traverse alignments
            print("hit:", hit)
            if bait not in map_dic:
                map_dic[bait] = {}
            # https://github.com/lh3/minimap2/tree/master/python
            # if hit.mapq >= args.mapq:
            map_dic[bait][C] = {"ctg": hit.ctg, "ctg_len": hit.ctg_len,
                          "r_st": hit.r_st, "r_en": hit.r_en, "strand": hit.strand,
                          "mapq": hit.mapq, "trans_strand": hit.trans_strand,
                          "is_primary": hit.is_primary,
                          "q_st": hit.q_st, "q_en": hit.q_en}

            C += 1
        C = 0
        if map_dic:
            print("map_dic:", map_dic)

    # open fasta, cut from start hut and re-organise, print out
    # dump metadata file of hits


        # k = edlib.align(baits[bait], seq, mode="HW", task="locations", k=args.missmatch)
        # print(k)
        # if k['locations']:
        #     start = k['locations'][0][0]
        #     end = k['locations'][0][1]
        #     score = k['editDistance']
        #     print("{} start={} end={} score={}".format(name, start, end, score))
        # print(l[start:]+l[:start])
        # get best hits
        # print(l[start:]+l[:start])

if __name__ == '__main__':
    main()
