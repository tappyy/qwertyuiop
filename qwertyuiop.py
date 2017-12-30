#!/usr/bin/env python
from benchmark import *
import os.path
import argparse
import pandas as pd

# todo
# detect search space size (find lowercase, uppercase, digits and punctuation in the string)
# add option for input txt file instead of pwd args

parser = argparse.ArgumentParser()
parser.add_argument("pwd", type=str, nargs='+', default=[],
                    help="The password to test")
parser.add_argument("-b", "--benchmark",
                    help="Perform a benchmark to get guess rate", action="store_true")
parser.add_argument("-o", "--output",
                    help="Filename to output to csv")

args = parser.parse_args()

# create config file if it doesn't exist
if not(os.path.isfile(CONFIG_FILE)):
    create_config_file()
else:
    if(args.benchmark):
        timed_brute_force()

guess_rate = int(get_guess_rate())
print('guess rate is {} guesses per second'.format(guess_rate))

# init lists for csv output
if(args.output):
    passwords = []
    crack_times = []
    search_spaces = []

for password in args.pwd:
    search_space = 26**len(password)
    crack_time_seconds = search_space / guess_rate

    if(args.output):
        passwords.append(password)
        crack_times.append('{:.3f}'.format(crack_time_seconds))
        search_spaces.append(search_space)

if(args.output):
    df_data = {'Password':passwords, 'Crack Time': crack_times, 'Search Space':search_spaces}
    df = pd.DataFrame(df_data)
    df.to_csv(args.output,index=False)
