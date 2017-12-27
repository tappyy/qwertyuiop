#!/usr/bin/env python
import string
import itertools
import time
import argparse

# begin program
pwd = "andrew"
iterations = 0
start = time.time()
parser = argparse.ArgumentParser()

for guess in itertools.product(string.ascii_lowercase, repeat=6):
    iterations += 1
    if(''.join(guess) == pwd):
        finish = time.time()
        time_taken = finish - start
        print("found password: " + str(''.join(guess)))
        print("took {} attempts and {:.2f} seconds".format(iterations, time_taken))
        average_guesses = iterations / time_taken
        print("average guesses per second: {:.0f}".format(average_guesses))

        # end program
        exit()
