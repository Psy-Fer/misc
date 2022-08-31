import argparse
import sys
import mappy as mp


'''
align read and print accuracy and identity
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
        description="split input fasta into individual files")
    #group = parser.add_mutually_exclusive_group()
    parser.add_argument("-f", "--fastq",
                        help="fastq file with reads")
    parser.add_argument("-r", "--reference",
                        help="output folder path")

    args = parser.parse_args()

    # print help if no arguments given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)


    a = mp.Aligner(args.reference, preset="map-ont")  # load or build index
    if not a: raise Exception("ERROR: failed to load/build index")
    p_s = "".join(["{}\t",]*15)
    print(p_s.format("read_id", "ctg", "ref_start", "ref_end", 
                      "strand", "length", "matches", "correct",
                      "ins", "dels", "subs", "mapq", "strand_coverage",
                      "identity", "accuracy"))

    for name, seq, qual in mp.fastx_read(args.fastq): # read a fasta/q sequence
        for hit in a.map(seq): # traverse alignments
            # print("{}\t{}\t{}\t{}".format(hit.ctg, hit.r_st, hit.r_en, hit.cigar_str)
            seqlen = len(seq)
            ins = sum(count for count, op in hit.cigar if op == 1)
            dels = sum(count for count, op in hit.cigar if op == 2)
            subs = hit.NM - ins - dels
            length = hit.blen
            matches = length - ins - dels
            correct = hit.mlen
            

            print(p_s.format(
                name,
                hit.ctg,
                hit.r_st,
                hit.r_en,
                '+' if hit.strand == +1 else '-',
                length, matches, correct,
                ins, dels, subs,
                hit.mapq,
                round((hit.q_en - hit.q_st) / seqlen, 2),
                round(correct / matches, 2),
                round(correct / length, 2),
            ))




if __name__ == '__main__':
    main()
