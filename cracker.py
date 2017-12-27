#!/usr/bin/env python
import string
import itertools
import time
import argparse

# todo
# display average guesses per second when attacking large passwords
# choose whether to perform a brute force or simulate it (default=simulate)
# output stats to csv file
# prettify output

# begin program
iterations = 0
start = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("pwd", type=str,
                    help='the password to test')

args = parser.parse_args()
password = args.pwd

print('Attempting to brute force: {}'.format(password))
for guess in itertools.product(string.ascii_lowercase, repeat=len(password)):
    iterations += 1
    print('>>> Attempts: {}'.format(iterations), end='\r', flush=True)
    if(''.join(guess) == password):
        finish = time.time()
        time_taken = finish - start
        average_guesses = iterations / time_taken
        print("found password in {:.2f} seconds ({} guesses) - avg guesses per second: {:.0f}".format(time_taken, iterations, average_guesses))

        # end program
        exit()
