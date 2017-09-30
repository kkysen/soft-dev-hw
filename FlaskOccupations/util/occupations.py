#!/usr/bin/python

"""
Khyber Sen, Shannon Lau
SoftDev1 pd7
HW3 -- StI/O: Divine your Destiny!
2017-09-13
"""

from __future__ import print_function

__authors__ = ['Khyber Sen', 'Shannon Lau']
__date__ = '2017-09-14'

import random
import csv
from collections import Counter


def _percentages(self):
    """
    An extension method for Counter that
    returns a dict mapping the keys of the Counter to their percentages.
    :param self: Counter
    :return: a dict mapping the keys of the Counter to their percentages
    """
    # type: () -> dict[any, float]
    length = float(sum(count for count in self.viewvalues()))
    return {value: self[value] / length for value in self}


Counter.percentages = _percentages


class Occupation(object):
    """
    :ivar name: str
    :ivar percent: float
    :ivar link: str | None
    """

    def __init__(self, parts):
        # type: (str) -> Occupation
        self.name = parts[0].strip('"')
        self.percent = float(parts[1])
        if len(parts) >= 3:
            self.link = parts[2]
        else:
            self.link = 'https://www.google.com/search?q=' + self.name


class Occupations(object):
    """
    :cvar DEFAULT_SAMPLE_SIZE: int
    :cvar UNITED_STATES_FILE: str
    :cvar __UNITED_STATES: Occupations

    :ivar occupations: list[Occupation]
    :ivar total_percent: float
    """

    DEFAULT_SAMPLE_SIZE = 1000000

    UNITED_STATES_FILE = 'data/occupations.csv'

    __UNITED_STATES = None  # lazy

    def __init__(self, file_name):
        """
        Create an Occupations object containing a list
        of the occupation, percent pairs, as well as
        the total percent, used to calculate weighted randomness.
        :param file_name: str
        """
        # type: str -> Occupations
        reader = csv.reader(open(file_name).read().splitlines()[1:-1], delimiter=',', quotechar='"')
        self.occupations = [Occupation(row) for row in reader]
        self.total_percent = sum(occupation.percent for occupation in self.occupations)

    def random_occupation(self):
        """
        Return a random occupation weighted by the percents of each.
        Occupations with higher percents are more likely to be returned.
        :return: a weighted random Occupation
        """
        # type: () -> Occupation
        random_percent = random.uniform(0, self.total_percent)  # type: float
        for occupation in self.occupations:
            if random_percent < occupation.percent:
                return occupation
            random_percent -= occupation.percent

    def random_occupation_name(self):
        # type () -> str
        return self.random_occupation().name

    def random_occupations(self, num_occupations):
        """
        Return a Counter of num_occupations chosen weighted randomly
        as by random_occupation.
        :param num_occupations: the number of occupations to return
        :return: a Counter of the random occupations
        """
        # type: int -> Counter
        return Counter(self.random_occupation_name() for i in xrange(num_occupations))

    def is_randomly_weighted(self, sample_size=DEFAULT_SAMPLE_SIZE, debug=False):
        """
        Determine if the random_occupation method is working correctly
        by sampling randomly weighted occupations and then comparing
        their statistical distribution with the percents by which
        the occupations are supposed to be weighted.
        :param sample_size: the number of occupations to sample
        :param debug: if the resulting chosen occupations
         and their statistical percents should be printed
        :return: true if the random_occupation method
        correctly Return random occupations weighted by their percents
        """
        # type: (int, bool) -> bool
        count = self.random_occupations(sample_size)
        delta = 0  # type: float
        percents = count.percentages()  # type: dict[str, float]
        for occupation in self.occupations:
            delta += abs(occupation.percent - percents.get(occupation.name, 0) * self.total_percent)
        if debug:
            print('\n'.join('{}: {} vs. {}'.format(occupation.name, occupation.percent,
                                                   percents[occupation.name] * self.total_percent)
                            for occupation, percent in self.occupations))
        estimate = 867.238 / sample_size ** (0.561231 * .95)
        accepted = 2 * estimate
        print('sample size: {:<8}: delta: {} < {}'.format(sample_size, delta, accepted))
        return delta < accepted

    @staticmethod
    def in_united_states():
        """
        Get an Occupations singleton from 'occupations.csv',
        which contains occupation data from the United States.
        :return: an Occupations singleton for the United States
        """
        # type: () -> Occupations
        if Occupations.__UNITED_STATES is None:
            Occupations.__UNITED_STATES = Occupations(Occupations.UNITED_STATES_FILE)
        return Occupations.__UNITED_STATES

    @staticmethod
    def test(sample_size=DEFAULT_SAMPLE_SIZE, debug=True):
        """
        Test if the United States Occupations is randomly_weighted.
        If not, it throws an AssertionError
        :param sample_size: the number of occupations to sample
        :param debug: if debug info should be printed
        """
        # type: (int, bool) ->
        error_msg = 'random weighted selection of occupations found in {}' \
                    ' is not working for a sample size of {}' \
            .format(Occupations.UNITED_STATES_FILE, sample_size)
        assert Occupations.in_united_states().is_randomly_weighted(sample_size, debug), error_msg


def test(sample_size=Occupations.DEFAULT_SAMPLE_SIZE, debug=True):
    """
    Call Occupations.test
    :param sample_size: the number of occupations to sample
    :param debug: if debug info should be printed
    """
    # type: (int, bool) ->
    Occupations.test(sample_size, debug)


def test_main():
    """
    Run test for sample sizes from 1e2 to 1e6 in powers of 10
    """
    # type: () ->
    million = True
    while True:
        for i in xrange(2, (6 if million else 5) + 1):
            test(debug=False, sample_size=10 ** i)
        print()


def main():
    """
    Print random occupation or test accuracy
    """
    # type: () ->
    try:
        option = int(raw_input(
            "0: Generate your future occupation. \n"
            "1: Test the accuracy of this generator. \n"
            "INPUT 0 OR 1: ").strip())
    except ValueError:
        print("Invalid entry.")
        return
    if option == 0:
        print(Occupations.in_united_states().random_occupation_name())
    elif option == 1:
        test_main()
    else:
        print("Invalid entry.")


if __name__ == '__main__':
    main()
