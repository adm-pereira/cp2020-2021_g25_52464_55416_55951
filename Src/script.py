import os
import re
import sys
import subprocess
import argparse
import configparser

def extract_tr(results):
    t = re.findall('(?<=Time: ).*', results)[0]
    r = ' '.join(re.findall('(?<=Result: ).*', results))
    return t, r

def run_command(command):
    #print(f'running: {command}')
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

def compare(seqoutput, ompoutput):
    seq_time, seq_results = extract_tr(seqoutput)
    omp_time, omp_results = extract_tr(ompoutput)
    if seq_results == omp_results:
        global sum_seq, sum_omp
        sum_seq += float(seq_time)
        sum_omp += float(omp_time)
        #print('outputs are equal')
        #print(f'Omp: {omp_time}')
        #print(f'Seq: {seq_time}')
        #ratio = float(omp_time)/float(seq_time) * 100
        #print(f'Parallel version time is %.2f of sequential version time' % ratio)
    else:
        print('Outputs differ!')
        print(f'Sequential ---> {seq_results}')
        print(f'Parallel   ---> {omp_results}')


sum_seq = 0.0
sum_omp = 0.0

#all tests
test_35 = 'test_files/test_01_a35_p8_w1 test_files/test_01_a35_p7_w2 test_files/test_01_a35_p5_w3 test_files/test_01_a35_p8_w4'
test_30k = 'test_files/test_02_a30k_p20k_w1 test_files/test_02_a30k_p20k_w2 test_files/test_02_a30k_p20k_w3'
#' test_files/test_02_a30k_p20k_w4 test_files/test_02_a30k_p20k_w5 test_files/test_02_a30k_p20k_w6' 

if __name__ == '__main__':

    number_tests = int(sys.argv[1])
    array_size = int(sys.argv[2])

    print(f'Using array size {array_size}\nRuns {number_tests} tests')
    
    for t in range(0, number_tests):
        if array_size == 35:
            str = f'./energy_storms_seq {array_size} ' + test_35
        else:
            str = f'./energy_storms_seq {array_size} ' + test_30k
        
        run_command('make energy_storms_seq')
        seqoutput = subprocess.check_output(str, shell=True).decode()
    
        if array_size == 35:
            str = f'./energy_storms_omp {array_size} ' + test_35
        else:
            str = f'./energy_storms_omp {array_size} ' + test_30k

        run_command('make energy_storms_omp')
        ompoutput = subprocess.check_output(str, shell=True).decode()
    
        compare(seqoutput, ompoutput)

    ratio = ((sum_seq/number_tests)/(sum_omp/number_tests)) * 100

    print(f'Average ratio SequentialTime/ParallelTime: %0.2f' % ratio)

    

