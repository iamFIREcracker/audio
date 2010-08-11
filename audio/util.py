#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module containing utility functions for audio processing.
"""

from __future__ import division

from numpy.fft import fft as _fft

        
def _nextpow(x, b):
    """Find the smallest integer p such that b ** p > x.
    """
    p = 1
    while p < x:
        p *= b
    return p

def fft(data):
    """Compute the fast Fourier transform on the input data.
    
    The normalized output is relative to the positive frequencies.
    
    Keywords:
        data list of data values.
        
    Return:
        Normalized fft.
    """
    N = len(data)
    M = _nextpow(len(data), 2)
    norm_factor = 2 / M
    data = norm_factor * _fft(data, M)
    return data[:N // 2]
