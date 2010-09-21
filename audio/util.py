#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module containing utility functions for audio processing.
"""

from __future__ import division
from itertools import islice
from itertools import chain

from numpy.fft import fft as _fft


def batch(iterable, size):
    """Split the iterable into batchs of given size.

    Keywords:
        iterable iterable to split.
        size max size of each returned batch (last one could be smaller).
    """
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield list(chain([batchiter.next()], batchiter))

def fft(data):
    """Compute the fast Fourier transform on the input data.

    The normalized output is relative to the positive frequencies and takes
    into account the power loss due to discarding half of the result.

    Keywords:
        data list of data values.

    Return:
        Normalized fft.
    """
    def nextpow(x, b):
        """Find the smallest integer p such that b ** p > x.
        """
        p = 0
        n = 1
        while n < x:
            n *= b
            p += 1
        return p

    N = len(data)
    M = 2 ** nextpow(len(data), 2)
    normfact = 1.4142135623730951 / N
    data = normfact * _fft(data, M)
    return data[:N // 2]
