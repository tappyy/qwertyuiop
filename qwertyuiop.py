#!/usr/bin/env python
import os.path
import argparse
import pandas as pd
import time
import configparser
import os
import string
import itertools
import argparse
import random
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

CONFIG_FILE = 'config.ini'
RANDOM_PASSWORD_LENGTH = 10

def main():
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
    logging.info('Guess rate per second: {}'.format(guess_rate))

    # init lists for csv output
    if(args.output):
        passwords = []
        crack_hours = []
        crack_days = []
        search_spaces = []

    # run through passwords file
    with open(args.pwdfile) as pf:
        logging.info('Analysing {}'.format(args.pwdfile))
        password = pf.readline().strip()
        while password:
            sample_space = get_search_space(password)
            total_search_space = sample_space**len(password)
            crack_time_hours = (total_search_space / guess_rate) / 60 / 60
            crack_time_days = crack_time_hours / 24

            if(args.output):
                passwords.append(password.strip())
                crack_hours.append('{:.2f}'.format(crack_time_hours))
                crack_days.append('{:.2f}'.format(crack_time_days))
                search_spaces.append('{}^{}'.format(sample_space, len(password)))

            password = pf.readline().strip()
    logging.info('Finished analysis.')

    # create dataframe and output csv
    if(args.output):
        df_data = {'Password':passwords,
                    'Crack Time H': crack_hours,
                    'Crack Time D':crack_days,
                    'Search Space':search_spaces}
        df = pd.DataFrame(df_data)
        df.to_csv(args.output, index = False)
        logging.info('Output saved to: {}'.format(args.output))

def get_guess_rate():
    if not(os.path.isfile(CONFIG_FILE)):
        logging.warning('Config file not found.')
        create_config_file()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    guess_rate = config.get('benchmark_settings', 'guess_rate')
    return guess_rate

def get_benchmark_guesses():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    guess_limit = config.get('benchmark_settings', 'benchmark_guesses')
    return guess_limit

def get_search_space(password):
    search_space = 0
    alphabet_length = 26
    digits_length = 10
    punctuation_length = 33

    lowercase_re = re.compile("[a-z]")
    uppercase_re = re.compile("[A-Z]")
    digits_re = re.compile("[0-9]")
    punc_re = re.compile(r"\W")

    if(lowercase_re.search(password)):
        search_space = search_space + alphabet_length

    if(uppercase_re.search(password)):
        search_space = search_space + alphabet_length

    if(digits_re.search(password)):
        search_space = search_space + digits_length

    if(punc_re.search(password)):
        search_space = search_space + punctuation_length

    return search_space

def timed_brute_force():
    logging.info('Performing brute force benchmark...')
    time_start = time.time()
    guesses = 0
    random_password = create_random_password()
    benchmark_guesses = int(get_benchmark_guesses())

    for guess in itertools.product(string.ascii_letters + string.punctuation, repeat=RANDOM_PASSWORD_LENGTH):
        guesses += 1
        if(guesses == benchmark_guesses):
            time_finish = time.time()
            time_taken = time_finish - time_start
            guess_rate = guesses / time_taken
            update_config_file('{:.0f}'.format(guess_rate))
            break
    logging.info('Brute force benchmark complete. Time taken: {:.2f}s'.format(time_taken))

def create_random_password():
    random_password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(RANDOM_PASSWORD_LENGTH)])
    return random_password

def create_config_file():
    logging.info('Creating config file: {}'.format(CONFIG_FILE))
    config = configparser.ConfigParser()
    config.add_section('benchmark_settings')
    config.set('benchmark_settings', 'guess_rate', str(0)) # default value
    config.set('benchmark_settings', 'benchmark_guesses', str(10000000)) # default value - 10 mil

    with open(CONFIG_FILE, "w") as f:
        config.write(f)

    logging.debug('Created file: {}'.format(CONFIG_FILE))

    timed_brute_force()

def update_config_file(guess_rate):
    logging.debug('Updating guess rate...')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    config.set('benchmark_settings', 'guess_rate', str(guess_rate))

    with open(CONFIG_FILE, "w") as f:
        config.write(f)

    logging.debug('Guess rate updated.')

if __name__ == '__main__':
    main()
