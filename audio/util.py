# -*- coding: Latin-1 -*-

"""Module containing utility functions for audio processing.
"""

from __future__ import division

from numpy import abs
from numpy import log10
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
    
    The output is the normalized magnitude of the values associated to the
    positive frequencies.
    
    Keywords:
        data list of data values.
        
    Return:
        Abs of the normalized fft.
    """
    N = len(data)
    M = _nextpow(len(data), 2)
    data = 20 * log10((abs(_fft(data, M)[:M // 2] + 1e-15) / M) / 32768)
    return data[:N]
