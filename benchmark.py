import time
import configparser
import os
import platform
import multiprocessing
import string
import itertools
import argparse
import random
import wmi

CONFIG_FILE = 'config.ini'
RANDOM_PASSWORD_LENGTH = 10
MAX_GUESS_LIMIT = 5000000
computer = wmi.WMI()
cpu_info = computer.Win32_Processor()[0]

def get_guess_rate():
    if not(os.path.isfile(CONFIG_FILE)):
        create_config_file()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    guess_rate = config.get('cpu_settings', 'guess_rate')
    return guess_rate

def timed_brute_force():
    # add progress bar
    time_start = time.time()
    guesses = 0
    random_password = create_random_password()
    print('CPU: {}'.format(str(cpu_info.Name)))
    print('Logical Cores: {}'.format(os.cpu_count()))
    print('Random password: {}'.format(random_password))

    for guess in itertools.product(string.ascii_letters + string.punctuation, repeat=RANDOM_PASSWORD_LENGTH):
        guesses += 1
        # print('>>> Attempts: {}'.format(guesses), end='\r', flush=True)
        if(guesses == MAX_GUESS_LIMIT):
            time_finish = time.time()
            time_taken = time_finish - time_start
            guess_rate = guesses / time_taken
            update_config_file('{:.0f}'.format(guess_rate))
            print('Guess target of {} reached. Guess rate per second: {:.0f} - Time taken: {:.2f} seconds'.format(MAX_GUESS_LIMIT, guess_rate, time_taken))
            break

def create_random_password():
    random_password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(RANDOM_PASSWORD_LENGTH)])
    return random_password

def create_config_file():
    computer = wmi.WMI()
    cpu_info = computer.Win32_Processor()[0]
    print('Creating .ini file')
    config = configparser.ConfigParser()
    config.add_section('cpu_settings')
    config.set('cpu_settings', 'cpu_model', str(cpu_info.Name))
    config.set('cpu_settings', 'cpu_logical', str(os.cpu_count()))
    config.set('cpu_settings', 'guess_rate', str(15000)) # default value

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
