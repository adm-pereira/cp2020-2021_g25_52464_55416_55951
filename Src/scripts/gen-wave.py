#!/bin/python3

import sys
import numpy as np
import argparse


def arg_parse():
    parser = argparse.ArgumentParser(
        description='Generate wave files for the simplified simulation of high-energy particle storms')
    # positional arguments
    parser.add_argument('n_particles', type=int, help='number of particles for the wave')
    parser.add_argument('position_max', type=int, help='max position value allowed')
    parser.add_argument('energy_max', type=int, help='max position value allowed')
    # optional arguments
    parser.add_argument('--mode', dest='mode', type=int, help='mode value for the positions')
    parser.add_argument('--out', dest='out', metavar='filename', help='output wave file')
    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parse()
    out = sys.stdout if args.out is None else open(args.out, 'w')

    if args.mode is None:
        positions = np.array(
            np.random.uniform(low=0, high=args.position_max, size=args.n_particles), dtype=int)
    else:
        positions = np.array(
            np.random.triangular(left=0, right=args.position_max, mode=args.mode, size=args.n_particles), dtype=int)

    energy_values = np.positions = np.array(
        np.random.uniform(low=0, high=args.energy_max, size=args.n_particles), dtype=int)

    out.write(f'{args.n_particles}\n')
    for pos, energy in zip(positions, energy_values):
        out.write(f'{pos} {energy}\n')