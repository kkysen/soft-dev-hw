#!/usr/bin/python

"""
Khyber Sen, Shannon Lau
SoftDev1 pd7
HW3 -- StI/O: Divine your Destiny!
2017-09-13
"""

from __future__ import print_function

import random

from collections import Counter

__authors__ = ['Khyber Sen', 'Shannon Lau']
__date__ = '2017-09-14'


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


class Occupations(object):
    """
    :cvar DEFAULT_SAMPLE_SIZE: int
    :cvar UNITED_STATES_FILE: str

    :ivar occupations: list[tuple[str, float]]
    :ivar total_percent: float
    """

    DEFAULT_SAMPLE_SIZE = 1000000

    UNITED_STATES_FILE = 'occupations.csv'

    @staticmethod
    def parse_line(line):
        """
        Parses a line from the occupations.csv file,
        where the first column is the occupation name
        (optionally quoted) and the second is the
        out of 100 percent for that occupation.
        :param line: line of csv file
        :return: pair of occupation and percent
        """
        # type: str -> tuple[str, float]
        occupation, percent = line.rsplit(',', 1)
        return occupation.strip('"'), float(percent)

    def __init__(self, file_name):
        """
        Creates an Occupations object containing a list
        of the occupation, percent pairs, as well as
        the total percent, used to calculate weighted randomness.
        :param file_name: str
        """
        # type: str -> Occupations
        self.occupations = [Occupations.parse_line(line) for line in
                            open(file_name).read().splitlines()[1:]]
        self.total_percent = sum(occupation[1] for occupation in self.occupations)

    def random_occupation(self):
        """
        Returns a random occupation weighted by the percents of each.
        Occupations with higher percents are more likely to be returned.
        :return: a weighted random occupation
        """
        # type: () -> str
        random_percent = random.uniform(0, self.total_percent)  # type: float
        for occupation, percent in self.occupations:
            if random_percent < percent:
                return occupation
            random_percent -= percent

    def random_occupations(self, num_occupations):
        """
        Returns a Counter of num_occupations chosen weighted randomly
        as by random_occupation.
        :param num_occupations: the number of occupations to return
        :return: a Counter of the random occupations
        """
        # type: int -> Counter
        return Counter(self.random_occupation() for i in xrange(num_occupations))

    def is_randomly_weighted(self, sample_size=DEFAULT_SAMPLE_SIZE, debug=False):
        """
        Determines if the random_occupation method is working correctly
        by sampling randomly weighted occupations and then comparing
        their statistical distribution with the percents by which
        the occupations are supposed to be weighted.
        :param sample_size: the number of occupations to sample
        :param debug: if the resulting chosen occupations
         and their statistical percents should be printed
        :return: true if the random_occupation method
        correctly returns random occupations weighted by their percents
        """
        # type: (int, bool) -> bool
        count = self.random_occupations(sample_size)
        delta = 0  # type: float
        percents = count.percentages()  # type: dict[str, float]
        for occupation, percent in self.occupations:
            delta += abs(percent - percents.get(occupation, 0) * self.total_percent)
        if debug:
            print('\n'.join('{}: {} vs. {}'.format(occupation, percent,
                                                   percents[occupation] * self.total_percent)
                            for occupation, percent in self.occupations))
        estimate = 867.238 / sample_size ** (0.561231 * .95)
        accepted = 2 * estimate
        print('sample size: {:<8}: delta: {} < {}'.format(sample_size, delta, accepted))
        return delta < accepted

    @staticmethod
    def in_united_states():
        """
        Creates an Occupations from 'occupations.csv',
        which contains occupation data from the United States.
        :return: an Occupations for the United States
        """
        # type: () -> Occupations
        return Occupations(Occupations.UNITED_STATES_FILE)

    @staticmethod
    def test(sample_size=DEFAULT_SAMPLE_SIZE, debug=True):
        """
        Tests if the United States Occupations is randomly_weighted.
        If not, it throws an AssertionError
        :param sample_size: the number of occupations to sample
        :param debug: if debug info should be printed
        """
        # type: (int, bool) -> None
        error_msg = 'random weighted selection of occupations found in {}' \
                    ' is not working for a sample size of {}' \
            .format(Occupations.UNITED_STATES_FILE, sample_size)
        assert Occupations.in_united_states().is_randomly_weighted(sample_size, debug), error_msg


def test(sample_size=Occupations.DEFAULT_SAMPLE_SIZE, debug=True):
    """
    Calls Occupations.test
    :param sample_size: the number of occupations to sample
    :param debug: if debug info should be printed
    """
    # type: (int, bool) ->
    Occupations.test(sample_size, debug)


def main():
    """
    Runs test for sample sizes from 1e2 to 1e6 in powers of 10
    """
    # type: () ->
    million = True
    while True:
        for i in xrange(2, (6 if million else 5) + 1):
            test(debug=False, sample_size=10 ** i)
        print()


if __name__ == '__main__':
    main()
