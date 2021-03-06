#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module containing widgets used to display audio signals.
"""

from __future__ import division

import cairo
import gtk
from numpy import abs
from numpy import log10
from numpy import pi
from numpy import sin

from audio.util import fft
from audio.util import batch


class Visualizer(gtk.DrawingArea):
    """Base class used by inheritance from the various specific visualizers.
    """

    def __init__(self):
        """Constructor.

        Create a drawing area used to display audio visualizations.
        """
        super(Visualizer, self).__init__()

        self.data = []
        self.surface = self.context = None

        self.connect('configure-event', self.configure_cb)
        self.connect('expose-event', self.expose_cb)

    def configure_cb(self, darea, event):
        """Create a private surface and its cairo context.
        """
        width, height = darea.window.get_size()
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                          width,
                                          height)
        self.context = cairo.Context(self.surface)
        self.context.scale(width / 2, height / 2)
        self.context.translate(1, 1)

        return True

    def expose_cb(self, darea, event):
        """Redraw either the whole window or a part of it.
        """
        context = darea.window.cairo_create()

        context.rectangle(event.area.x, event.area.y,
                          event.area.width, event.area.height)
        context.clip()
        context.set_source_surface(self.surface, 0, 0)
        context.paint()

        return False

    def draw(self, context):
        """Redraw the drawing area.

        Keywords:
            context surface used for drawing actions.
        """
        pass

    def refresh(self, data):
        """Refresh the data displayed on screen.

        Keywords:
            data list of values supposed to be bounded between -(2 ** 15) and
                 ((2 ** 15) - 1).
        """
        self.data[:] = data
        self.draw(self.context)
        self.queue_draw()


class Analyzer(Visualizer):
    """Display the spectrum analyzer of the input audio signal.
    """

    def __init__(self, threshold=-60, bands=128):
        """Constructor.

        Keywords:
            threshold threshold value (in dB) used to display fft data.
            bands number of output values extracted from fft.
        """
        super(Analyzer, self).__init__()

        self.threshold = threshold
        self.bands = bands

    def draw(self, context):
        """Redraw the drawing area.

        Keywords:
            context surface used for drawing actions.
        """
        context.set_source_rgb(0, 0, 0)
        context.rectangle(-1, -1, 2, 2)
        context.fill()

        threshold = self.threshold
        bands = self.bands
        data = self.data

        # compute the fft and trasform it in decibel notation:
        # - add 1e-15 in order to prevent log10(0).
        # - we divide by 1 because it is supposed to be the highest peak.
        data = 20 * log10(abs(fft(data) + 1e-15) / 1)

        # how many values we have to merge in order to achieve the desired
        # number of bands
        group = len(data) / bands
        data = [sum(seq) / len(seq) for seq in batch(data, group)]

        # is it possible to obtain more values that needed; we simply ignore
        # them (they refer to high value of frequencies.
        data[:] = data[:bands]

        ## data = 20 * log10(abs(fft(data[:512]) + 1e-15) / 1)
        ## temp = []
        ## data = [max(data[2 ** i:2 ** (i + 1)]) for i in xrange(8)]

        # color stuff.
        context.set_source_rgb(.8, .8, .8)

        # actual rendering.
        width = 2 / len(data)
        context.set_line_width(width)

        x = -1 + width / 2
        for value in data:
            context.move_to(x, 1)
            if value < threshold:
                value = threshold
            y = 1 - (value - threshold) / (-threshold) * 2
            context.line_to(x, y)

            context.stroke()
            x += width


class Oscilloscope(Visualizer):
    """Display the shape of the input audio signal.
    """

    def __init__(self, fill=False):
        """Constructor.

        Keywords:
            fill flag indicating wether to fill or not the audio shape.
        """
        super(Oscilloscope, self).__init__()

        self.fill = fill

    def draw(self, context):
        """Redraw the drawing area.

        Keywords:
            context surface used for drawing actions.
        """
        context.set_source_rgb(0, 0, 0)
        context.rectangle(-1, -1, 2, 2)
        context.fill()

        fill = self.fill
        data = self.data

        group = len(data) / 256
        data = [sum(seq) / len(seq) for seq in batch(data, group)]

        # color stuff.
        context.set_source_rgb(.8, .8, .8)

        # actual rendering.
        width = 2 / len(data)
        context.set_line_width(width)

        x = -1 + width / 2
        context.move_to(x, 0)
        for value in data:
            y = -value
            context.line_to(x, y)
            x += width
        context.line_to(1 - width / 2, 0)
        if fill:
            context.fill()
        else:
            context.stroke()
