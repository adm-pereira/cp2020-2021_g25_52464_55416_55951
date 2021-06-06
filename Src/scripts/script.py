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
        ratio = (float(seq_time)/float(omp_time) * 100.0) - 100
        #print(f'Parallel version time is %.2f of sequential version time' % ratio)
        return ratio
    else:
        print('Outputs differ!')
        print(f'Sequential ---> {seq_results}')
        print(f'Parallel   ---> {omp_results}')
        return -1


sum_seq = 0.0
sum_omp = 0.0

#all tests
test_1 = 'test_files/test_01_a35_p5_w3 test_files/test_01_a35_p7_w2 test_files/test_01_a35_p8_w1 test_files/test_01_a35_p8_w4'
array_1 = 35
test_2 = 'test_files/test_02_a30k_p20k_w1 test_files/test_02_a30k_p20k_w2 test_files/test_02_a30k_p20k_w3 test_files/test_02_a30k_p20k_w4 test_files/test_02_a30k_p20k_w5 test_files/test_02_a30k_p20k_w6'
array_2 = 30000
test_3 = 'test_files/test_03_a20_p4_w1'
array_3 = 20
test_4 = 'test_files/test_04_a20_p4_w1'
array_4 = 20
test_5 = 'test_files/test_05_a20_p4_w1'
array_5 = 20
test_6 = 'test_files/test_06_a20_p4_w1'
array_6 = 20
test_7 = 'test_files/test_07_a1M_p5k_w1 test_files/test_07_a1M_p5k_w2 test_files/test_07_a1M_p5k_w3 test_files/test_07_a1M_p5k_w4'
array_7 = 1000000
test_8 = 'test_files/test_08_a100M_p1_w1 test_files/test_08_a100M_p1_w2 test_files/test_08_a100M_p1_w3'
array_8 = 100000000
test_9 = 'test_files/test_09_a16-17_p3_w1'
array_9 = 17

if __name__ == '__main__':

    nTests = int(sys.argv[1])
    test_number = int(sys.argv[2])

    print(f'Running tests: 1-{test_number}, {nTests} time(s)')
    
    total_average = 0.0
    for t in range(0, nTests):

        iteration_average = 0.0

        for n in range(1, (test_number + 1)):
            test_input = ""
            array_input = 0
            exec('test_input = test_%d' % n)
            exec('array_input = array_%d' % n)

            str = f'./energy_storms_seq {array_input} ' + test_input
            run_command('make energy_storms_seq')
            seqoutput = subprocess.check_output(str, shell=True).decode()

            str = f'./energy_storms_omp {array_input} ' + test_input
            run_command('make energy_storms_omp')
            ompoutput = subprocess.check_output(str, shell=True).decode()

            iteration_average += compare(seqoutput, ompoutput)

        total_average += iteration_average / test_number
        
    ratio = total_average / nTests
    print('Average ratio ParallelTime is %0.2f percent faster than SequentialTime' % ratio)
    

