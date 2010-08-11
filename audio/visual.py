# -*- coding: Latin-1 -*-

"""Module containing widgets used to display audio signals.
"""

from __future__ import division
from math import log10

import cairo
import gtk

from audio.util import fft


class Visualizer(gtk.Window):
    """Base class used by inheritance from the various specific visualizers.
    """

    def __init__(self):
        """Constructor.
        
        Create a drawing area used to display audio visualizations.
        """
        super(Visualizer, self).__init__()
        
        self.data = []
        self.surface = self.context = None
        darea = gtk.DrawingArea()
        
        darea.connect('configure-event', self.configure_cb)
        darea.connect('expose-event', self.expose_cb)
        self.add(darea)
        self.show_all()

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
        self.context.set_line_width(0.005)
        
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
    
    def draw(self, context, data):
        """Redraw the drawing area.
        
        Keywords:
            context surface used for drawing actions.
            data list of data to be visualized.
        """
        pass

    def refresh(self, data):
        """Refresh the data displayed on screen.
        
        Keywords:
            data list of values supposed to be bounded between -(2 ** 15) and
                 ((2 ** 15) - 1).
        """
        self.draw(self.context, data)
        self.queue_draw()


class Analyzer(Visualizer):
    """Display the spectrum analyzer of the input audio signal.
    """
    
    def draw(self, context, data):
        """Redraw the drawing area.
        
        Keywords:
            context surface used for drawing actions.
            data list of data to be visualized.
        """
        context.set_source_rgb(0, 0, 0)
        context.rectangle(-1, -1, 2, 2)
        context.fill()
        context.set_source_rgb(1, 1, 1)
        
        threshold = -60 # decibel
        data = fft(data)
        width = 2 / len(data)
        context.set_line_width(width)
        x = -1
        for value in data:
            context.move_to(x, 1)
            if value < threshold:
                value = threshold
            y = 1 - (value - threshold) / (-threshold) * 2
            context.line_to(x, y)
            x += width
        context.stroke()
    
    
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
    
    def draw(self, context, data):
        """Redraw the drawing area.
        
        Keywords:
            context surface used for drawing actions.
            data list of data to be visualized.
        """
        context.set_source_rgb(0, 0, 0)
        context.rectangle(-1, -1, 2, 2)
        context.fill()
        
        context.set_source_rgb(1, 0, 1)
        width = 2 / len(data)
        x = -1
        for value in data:
            y = -value / 32768
            context.line_to(x, y)
            context.move_to(x, y)
            x += width
        context.stroke()
