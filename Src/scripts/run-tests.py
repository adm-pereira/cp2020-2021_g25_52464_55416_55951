#!/bin/python3

import os
import re
import subprocess
import argparse
import configparser
from progress.bar import IncrementalBar

# Executables
ENERGY_STORM_SEQ = './energy_storms_seq'
ENERGY_STORM_OMP = './energy_storms_omp'


def run_command(command):
    print(f'running: {command}')
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)


def arg_parse():
    parser = argparse.ArgumentParser(description='Run experiments defined on the provided configuration file')

    # positional arguments
    parser.add_argument('properties_file', help='configuration file name')
    parser.add_argument('experiment_list', metavar='experiment', action='store', nargs='+',
                        help='list of experiment section (must be defined on the config file)')
    # optional arguments
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='run debug tests')
    parser.add_argument('--output-dir', dest='out_dir', default='logs', help='logs directory')
    return parser.parse_args()


def extract_tr(results):
    t = re.findall('(?<=Time: ).*', results)[0]
    r = ' '.join(re.findall('(?<=Result: ).*', results))
    return t, r


def compare_and_log_output(test_section, seq_out, omp_out):
    # compare output
    if seq_out.split('Time')[0] == omp_out.split('Time')[0]:
        return  # test passed

    # test failed
    with open(f'{args.out_dir}/{test_section}_seq_debug.out', 'w') as log:
        log.write(seq_out)
    with open(f'{args.out_dir}/{test_section}_omp_debug.out', 'w') as log:
        log.write(omp_out)
    exit()


def exec_test(test_section, debug_mode=False, log=''):
    num_threads = config[test_section]['num_threads'].split()
    array_size = config[test_section]['array_size'].split()
    wave_files = ' '.join(config[test_section]['test_files'].split())

    for a in array_size:
        seq = subprocess.check_output(f'{ENERGY_STORM_SEQ} {a} {wave_files}', shell=True).decode()
        seq_time, seq_results = extract_tr(seq)
        for t in num_threads:
            omp = subprocess.check_output(f'{ENERGY_STORM_OMP} {t} {a} {wave_files}', shell=True).decode()
            if debug_mode:
                compare_and_log_output(test_section, seq, omp)
                return

            omp_time, omp_results = extract_tr(omp)
            log.write(f'omp,{a},{t},{omp_time},{omp_results}\n')

        log.write(f'seq,{a},_,{seq_time},{seq_results}\n')


if __name__ == '__main__':
    args = arg_parse()
    config = configparser.ConfigParser()
    os.makedirs(args.out_dir, exist_ok=True)

    print(f'reading: {args.properties_file}')
    config.read(args.properties_file)

    run_command('make clean')

    if args.debug:
        run_command('make debug_all')
        debug_tests = config['debug']['tests'].split()
        print()
        bar = IncrementalBar(f'Debug: {debug_tests}'.ljust(40), max=len(debug_tests),
                             suffix='%(percent)d%% - %(elapsed)ds')
        for test in debug_tests:
            exec_test(test, debug_mode=True)
            bar.next()
        bar.finish()

    run_command('make clean')
    run_command('make all')
    print(f'\nExperiments: {args.experiment_list}')
    for experiment in args.experiment_list:
        repetitions = config[experiment]['repetitions']
        tests = config[experiment]['tests'].split()
        bar = IncrementalBar(f'- {experiment}'.ljust(40), max=len(tests),
                             suffix='%(percent)d%% - %(elapsed)ds')

        for test in tests:
            os.makedirs(f'{args.out_dir}/{experiment}', exist_ok=True)
            with open(f'{args.out_dir}/{experiment}/{test}.csv', 'w') as csv:
                csv.write('version,array_size,num_threads,time,results\n')
                for run in range(int(repetitions)):
                    exec_test(test, log=csv)
            bar.next()
        bar.finish()