#!/usr/bin/env python
import string
import itertools
import time
import argparse

# begin program
iterations = 0
start = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("pwd", type=str,
                    help='the password to test')

args = parser.parse_args()
password = args.pwd

for guess in itertools.product(string.ascii_lowercase, repeat=len(password)):
    iterations += 1
    if(''.join(guess) == password):
        finish = time.time()
        time_taken = finish - start
        print("found password: " + str(''.join(guess)))
        print("took {} attempts and {:.2f} seconds".format(iterations, time_taken))
        average_guesses = iterations / time_taken
        print("average guesses per second: {:.0f}".format(average_guesses))

        # end program
        exit()
