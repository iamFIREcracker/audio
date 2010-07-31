#!/usr/bin/python
# -*- coding: Latin-1 -*-

"""Module containing utility functions for audio processing.
"""

from __future__ import division

import numpy


def fft(data):
    """Compute the fft of the input data.
    
    The returned list of values is normalized by a coefficient 2/N with N
    number of input samples, and is relative to positive values of frequencies.
    
    Keywords:
        data List of values bounded between -1 and +1.
        
    Return:
        Normalized fft.
    """
    N = len(data)
    return 2 / N * numpy.fft.fft(data)[:N // 2]