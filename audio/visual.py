# -*- coding: Latin-1 -*-

"""Module containing widgets used to display audio signals.
"""

from __future__ import division
from math import log10

import cairo
import gtk

from util import fft


class Visualizer(gtk.Window):
    """Base class used by inheritance from the various specific visualizers.
    """

    def __init__(self):
        """Constructor.
        
        Create a drawing area used to display audio visualizations.
        """
        super(Visualizer, self).__init__()
        
        darea = gtk.DrawingArea()
        darea.connect('configure-event', self.configure_cb)
        darea.connect('expose-event', self.expose_cb)
        self.add(darea)
        
        self.show_all()

    def configure_cb(self, darea, event):
        """Update the cairo context used for the drawing actions.
        """
        _, _, self.width, self.height = darea.get_allocation()
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                          self.width,
                                          self.height)
        self.cr = cairo.Context(self.surface)
        return True
    
    def expose_cb(self, darea, event):
        """Redraw either the whole window or a part of it.
        """
        cr = darea.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                     event.area.width, event.area.height)
        cr.clip()
        cr.set_source_surface(self.surface, 0, 0)
        cr.paint()
        return False
    
    def draw(self, data):
        """Draw input data on the surface object.
        
        Keywords:
            cr cairo context used for drawing purposes.
            data list of values bounded between -1 and +1.
        """
        pass

    def refresh(self, data):
        """Refresh the data displayed on screen.
        
        Keywords:
            data list of values bounded between -1 and +1.
        """
        self.draw(self.cr, self.width, self.height, data)
        self.queue_draw()


class Analyzer(Visualizer):
    """Display the spectrum analyzer of the input audio signal.
    """
    
    def draw(self, cr, cr_width, cr_height, data):
        """
        Compute the fft, normalize it by a coefficient of 2/N, then draw a
        vertical line for each component of the signal.
        
        Keywords:
            cr cairo context used for drawing purposes.
            cr_width width of the cairo context.
            cr_height height of the cairo context.
            data list of values bounded between -1 and +1.
        """
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, cr_width, cr_height)
        cr.fill()
        
        cr.set_source_rgb(0, 0, 0)
        samples = len(data)
        step = self.width / (samples // 2)
        scale_factor = 1024
        for (i, value) in enumerate(map(abs, fft(data))):
            value = log10(value * scale_factor + 1) / log10(scale_factor)
            x = i * step
            y = -value * self.height
            cr.move_to(x, self.height - 1)
            cr.rel_line_to(0, y)
            cr.stroke()
    
    
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
    
    def draw(self, cr, cr_width, cr_height, data):
        """
        Connect the points of the input signal by simple lines.
        
        Keywords:
            cr cairo context used for drawing purposes.
            cr_width width of the cairo context.
            cr_height height of the cairo context.
            data list of values bounded between -1 and +1.
            data List containing the values of the input signal.
        """
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, cr_width, cr_height)
        cr.fill()
        
        cr.set_source_rgb(0, 0, 0)
        samples = len(data)
        step = (cr_width - 1) / (samples // 2)
        cr.move_to(0, cr_height // 2)
        for (i, y) in enumerate(data):
            x = i * step
            y = -y * (cr_height // 2)
            cr.line_to(x, cr_height // 2 + y)
        cr.line_to(cr_width - 1, cr_height // 2)
        cr.fill() if self.fill else cr.stroke()
