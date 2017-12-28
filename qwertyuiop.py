#!/usr/bin/env python
from benchmark import get_guess_rate
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pwd", type=str,
                    help='the password to test')

args = parser.parse_args()
password = args.pwd
guess_rate = get_guess_rate()
print('guess rate is {} guesses per second'.format(guess_rate))

# calculate time to brute force password given guess rate
