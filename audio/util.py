# -*- coding: Latin-1 -*-

"""Module containing utility functions for audio processing.
"""

from __future__ import division

from numpy import abs
from numpy import log10
from numpy.fft import fft as _fft


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
    return 20 * log10((abs(_fft(data)[:N // 2] + 1e-15) / N) / 32768)
