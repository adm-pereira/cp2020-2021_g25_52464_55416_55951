import os
import re
import subprocess
import argparse
import configparser

def extract_tr(results):
    t = re.findall('(?<=Time: ).*', results)[0]
    r = ' '.join(re.findall('(?<=Result: ).*', results))
    return t, r

def run_command(command):
    print(f'running: {command}')
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)


print(f'Using array size 35')

run_command('make energy_storms_seq')
seqoutput = subprocess.check_output('./energy_storms_seq 35 test_files/test_01_a35_p8_w1 test_files/test_01_a35_p7_w2 test_files/test_01_a35_p5_w3', shell=True).decode()
seq_time, seq_results = extract_tr(seqoutput)
print(f'results: {seq_time} {seq_results}')

run_command('make energy_storms_omp')
ompoutput = subprocess.check_output('./energy_storms_omp 35 test_files/test_01_a35_p8_w1 test_files/test_01_a35_p7_w2 test_files/test_01_a35_p5_w3', shell=True).decode()
omp_time, omp_results = extract_tr(ompoutput)
print(f'results: {omp_time} {omp_results}')