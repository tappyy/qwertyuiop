#!/usr/bin/env python
from benchmark import *
import os.path
import argparse

# add output to csv option
parser = argparse.ArgumentParser()
parser.add_argument("pwd", type=str,
                    help="The password to test")
parser.add_argument("-b", "--benchmark",
                    help="Perform a benchmark to get guess rate", action="store_true")

args = parser.parse_args()
password = args.pwd

# create config file if it doesn't exist
if not(os.path.isfile(CONFIG_FILE)):
    create_config_file()
else:
    if(args.benchmark): # stops performing benchmark twice
        timed_brute_force()

guess_rate = int(get_guess_rate())
search_space = 26**len(password)
print('guess rate is {} guesses per second'.format(guess_rate))

crack_time_seconds = search_space / guess_rate
crack_time_minutes = crack_time_seconds / 60
crack_time_hours = crack_time_minutes / 60
crack_time_days = crack_time_hours / 24

print('Estimated time to crack password: {:.2f} seconds or {:.2f} minutes or {:.2f} hours or {:.2f} days'.format(crack_time_seconds, crack_time_minutes, crack_time_hours, crack_time_days))

# calculate time to brute force password with given guess rate
# lowercase 6 letter: password = 26^6 = 308915776 search space
# guess rate of 15000/second
# 308,915,776 / 15000 = 20594 seconds to search entire space
