import time
import configparser
import os
import string
import itertools
import argparse
import random

# todo
# format outputs
# add progress feedback

CONFIG_FILE = 'config.ini'
RANDOM_PASSWORD_LENGTH = 10

def get_guess_rate():
    if not(os.path.isfile(CONFIG_FILE)):
        create_config_file()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    guess_rate = config.get('cpu_settings', 'guess_rate')
    return guess_rate

def get_benchmark_guesses():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    guess_limit = config.get('general_settings', 'benchmark_guesses')
    return guess_limit

def timed_brute_force():
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
            print('Guess target of {} reached. Guess rate per second: {:.0f} - Time taken: {:.2f} seconds'.format(benchmark_guesses, guess_rate, time_taken))
            break

def create_random_password():
    random_password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(RANDOM_PASSWORD_LENGTH)])
    return random_password

def create_config_file():
    print('Creating .ini file')
    config = configparser.ConfigParser()
    config.add_section('benchmark_settings')
    config.set('cpu_settings', 'guess_rate', str(0)) # default value

    config.add_section('general_settings')
    config.set('general_settings', 'benchmark_guesses', str(10000000)) # default value - 10 mil

    with open(CONFIG_FILE, "w") as f:
        config.write(f)

    print('.ini file created')

    timed_brute_force()

def update_config_file(guess_rate):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    config.set('cpu_settings', 'guess_rate', str(guess_rate))

    with open(CONFIG_FILE, "w") as f:
        config.write(f)
