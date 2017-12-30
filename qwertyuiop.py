#!/usr/bin/env python
from benchmark import *
import os.path
import argparse
import pandas as pd

# todo
# detect search space size (find lowercase, uppercase, digits and punctuation in the string)
# add option for input txt file instead of pwd args

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="pwdfile", required=True,
                    help="File containing passwords to test")
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
    crack_hours = []
    crack_days = []
    search_spaces = []

# run through passwords file
with open(args.pwdfile) as pf:
    password = pf.readline().strip()
    while password:
        search_space = 26**len(password)
        crack_time_hours = (search_space / guess_rate) / 60 / 60
        crack_time_days = crack_time_hours / 24

        if(args.output):
            passwords.append(password.strip())
            crack_hours.append('{:.2f}'.format(crack_time_hours))
            crack_days.append('{:.2f}'.format(crack_time_days))
            search_spaces.append('26^{}'.format(len(password)))

        password = pf.readline().strip()

# create dataframe and output csv
if(args.output):
    df_data = {'Password':passwords,
                'Crack Time H': crack_hours,
                'Crack Time D':crack_days,
                'Search Space':search_spaces}
    df = pd.DataFrame(df_data)
    df.to_csv(args.output,index=False)
