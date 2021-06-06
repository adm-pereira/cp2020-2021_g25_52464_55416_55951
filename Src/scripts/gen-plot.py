#!/bin/python3

import os
import pandas
import matplotlib.pyplot as plt
import argparse


def arg_parse():
    parser = argparse.ArgumentParser(description='Process results from experiments')

    # optional arguments
    parser.add_argument('--experiments', metavar='E', dest='experiments', action='store', nargs='+',
                        help='list experiments to process')
    parser.add_argument('--input-dir', dest='in_dir', default='logs',
                        help='experiment logs directory (default=./logs)')
    parser.add_argument('--output-dir', dest='out_dir', default='plots',
                        help='directory to store the plots (default=./plots)')
    return parser.parse_args()


def joint_plot(figname, title, x_axis, y_axis):
    plt.figure()
    for label in y_axis:
        plt.plot(x_axis, y_axis[label], '-o', label=label)
    plt.xlabel('Number of threads')
    plt.ylabel('Execution time (s)')
    plt.legend()
    plt.title(title)
    # plt.show()
    plt.savefig(f'{figname}')


def process_experiment(experiment_name):
    tests = get_files(f'{args.in_dir}/{experiment_name}')
    os.makedirs(f'{args.out_dir}/{experiment_name}', exist_ok=True)
    for test in tests:
        input_csv = f'{args.in_dir}/{experiment_name}/{test}'
        output_plot = f'{args.out_dir}/{experiment_name}/{test.split(".")[0]}.jpg'
        dataframe = pandas.read_csv(input_csv)
        groups = dataframe.groupby(['version', 'num_threads'])

        num_threads = dataframe['num_threads'].unique().tolist()
        num_threads.remove('_')

        exec_times = dict()
        exec_times['seq'] = [groups.get_group(('seq', '_'))['time'].mean()] * len(num_threads)
        exec_times['omp'] = list()
        for num in num_threads:
            exec_times['omp'].append(groups.get_group(('omp', num))['time'].mean())

        joint_plot(output_plot, f'{experiment_name} - {test.split(".")[0]}', num_threads, exec_times)


def get_dirs(path):
    return [file.name for file in os.scandir(path) if file.is_dir()]


def get_files(path):
    return [file.name for file in os.scandir(path) if file.is_file()]


if __name__ == '__main__':
    args = arg_parse()
    experiments = get_dirs(args.in_dir) if args.experiments is None else args.experiments

    print(f'Processing results in {args.in_dir}...')
    for experiment in experiments:
        process_experiment(experiment)
        print(f'Plots from {experiment} available at {args.out_dir}/{experiment}')