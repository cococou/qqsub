#!/usr/bin/env python3
# coding: utf-8

import os,sys,re,hashlib
import gzip
import getopt


def xopen_fq(file,mode='r'):
    #sub of check_fastq
    if file.endswith(".gz"):
        return gzip.open(file, mode)
    else:
        return open(file,mode)
def PAR(argv):
    Pardic = {}
    opts, args = getopt.getopt(argv[1:], 'h',['indir=','id=','fq1=','fq2='])
    for o,a in opts:
        if o in ('-h'):
            print("indir id fq1 fq2")
            exit()
        elif o in ('--indir'):
            Pardic.update({'indir':a})
        elif o in('--id'):
            Pardic.update({'id':a})
        elif o in ('--fq1'):
            Pardic.update({'fq1':a})
        elif o in ('--fq2'):
            Pardic.update({'fq2':a})
        else:
            print('unhandled option')
            exit(1)
    return Pardic

def find_sample(Pardic):
    fq1 = []
    all = os.listdir(Pardic['indir'])
    img1 = re.compile(Pardic['id']+".*R1.fastq.gz$")
    for i in all:
        if  img1.findall(i):
            fq1.append(i)
    fq2 = [i.replace("R1.fastq","R2.fastq") for i in fq1]
    fq1 = [os.path.join(Pardic['indir'],i) for i in fq1]
    fq2 = [os.path.join(Pardic['indir'],i) for i in fq2]
    return fq1,fq2

def check_fastq(argv):
    Pardic = PAR(argv)
    fq1s,fq2s = find_sample(Pardic)
    fq1out = Pardic['fq1']
    fq2out = Pardic['fq2']

    f1 = open(fq1out,"w")
    f2 = open(fq2out,"w")

    for fq1 in fq1s:
        print(fq1)
        fq2 = fq1.replace("R1.fastq","R2.fastq")
        if fq1.endswith(".gz"):
            gz = True
        else:
            gz = False

        L1 = []; L2 = []

        for line1,line2 in zip(xopen_fq(fq1),xopen_fq(fq2)):

            if gz:
                line1 = line1.rstrip().decode('utf-8')
                line2 = line2.rstrip().decode('utf-8')
            else:
                line1 = line1.rstrip()
                line2 = line2.rstrip()

            if line1.startswith("@"):
                if  L1:
                    if len(L1[1]) != len(L1[3]):
                        print("fq1:base length is not equal with quality length",L1[1],L1[3],file=std.err)
                        exit(1)
                    if len(L1[1]) != len(L2[1]):
                        print("base length is not equal between two fastq files",L1[1],L2[1],file=std.err)
                        exit(1)
                    if len(L2[1]) != len(L2[3]):
                        print("fq2:base length is not equal with quality length",L2[1],L2[3],file=std.err)
                        exit(1)
                    tag1 = L1[1][9:19]
                    tag2 = L2[1][9:19]
                    tag = '@' + tag1 + tag2 + '|'
                    L1[0] = tag + L1[0][1:]
                    L2[0] = tag + L2[0][1:]
                    L1_s = '\n'.join(L1);L2_s = '\n'.join(L2)
                    print(L1_s,file = f1)
                    print(L2_s,file = f2 )

                    L1 = []
                    L2 = []

                L1.append(line1)
                L2.append(line2)
            elif  line1 != '+':
                L1.append(line1)
                L2.append(line2)
            elif  line1 == '+':
                L1.append(line1)
                L2.append(line2)
            else:
                L1.append(line1)
                L2.append(line2)




if __name__ == '__main__':
    check_fastq(sys.argv)
