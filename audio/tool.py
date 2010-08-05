# -*- coding: Latin-1 -*-

"""Module containing an helper widgets.
"""

from __future__ import division
from math import pi

import cairo
import gobject
import gtk
from gtk import gdk


class Pad(gtk.Window):
    """Widget used to generate pairs of coordinate values.
    
    Create a drawing area connected to mouse events. Generate a couple of
    values between -1 and +1 depending on the position of the mouse during a 
    drag and drop operation.
    """
    
    __gsignals__ = {
            'start-dnd': (gobject.SIGNAL_RUN_FIRST, None, ()),
            'dnd-value': (gobject.SIGNAL_RUN_FIRST, None,
                (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)),
            'end-dnd': (gobject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        """Constructor.
        
        Create a drawing area and connect to mouse events.
        """
        super(Pad, self).__init__()

        self.oldx, self.oldy = -1, -1
        self.width, self.height = -1, -1
        self.surface, self.cr = None, None

        darea = gtk.DrawingArea()
        darea.add_events(gdk.BUTTON_PRESS_MASK
                              | gdk.BUTTON_RELEASE_MASK
                              | gdk.POINTER_MOTION_MASK
                              | gdk.POINTER_MOTION_HINT_MASK)
        darea.connect('button-press-event', self.button_press_cb)
        darea.connect('button-release-event', self.button_release_cb)
        darea.connect('configure-event', self.configure_cb)
        darea.connect('expose-event', self.expose_cb)
        darea.connect('motion_notify_event', self.motion_notify_cb)
        self.add(darea)
        self.show_all()

    def button_press_cb(self, darea, event):
        """Notify the beginning of a drag and drop event.
        """
        x, y = event.x, event.y
        self.draw_pointer(self.cr, x, y)
        self.queue_draw()
        self.oldx, self.oldy = x, y
        rel_x, rel_y = self.absolute_to_relative(x, y)
        self.emit('dnd-value', rel_x, rel_y)
        self.emit('start-dnd')
        return True

    def button_release_cb(self, darea, event):
        """Notify the end of a drag and trop event.
        """
        self.oldx, self.oldy = event.x, event.y
        self.draw_pointer(self.cr, None, None)
        self.queue_draw()
        self.oldx, self.oldy = None, None
        self.emit('end-dnd')
        return True

    def configure_cb(self, darea, event):
        """Update the cairo context used for the drawing actions.
        """
        self.width, self.height = darea.window.get_size()
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width,
                                          self.height)
        self.cr = cairo.Context(self.surface)
        self.draw(self.cr, self.width, self.height)
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
    
    def motion_notify_cb(self, darea, event):
        """Emit a new drag and drop value.
        """
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        if state & gdk.BUTTON1_MASK or state & gdk.BUTTON3_MASK:
            self.draw_pointer(self.cr, x, y)
            self.queue_draw()
            self.oldx, self.oldy = x, y
            rel_x, rel_y = self.absolute_to_relative(x, y)
            self.emit('dnd-value', rel_x, rel_y)
        return True

    def draw(self, cr, width, height):
        """Draw the white background of the pad widget.
        
        Keywords:
            cr cairo context used for drawing operations.
            width width of the cairo context.
            height height of the cairo context.
        """
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()

    def draw_pointer(self, cr, newx, newy):
        """Draw a circle surrounding the the pointer.
        
        Keywords:
            cr cairo context.
            newx new x coordinate of the pointer.
            newy new y coordinate of the pointer.
        """
        data = [(self.oldx, self.oldy, 15, (1, 1, 1)),
                (newx, newy, 10, (0, 1, 0))]
        for (x, y, radius, (r, g, b)) in data:
            if x and y:
                cr.set_source_rgb(r, g, b)
                cr.arc(x, y, radius, 0, 2 * pi)
                cr.fill()

    def absolute_to_relative(self, x, y):
        """Convert given coordinate from absolute to relative.
        
        The returned coordinates are relative to the center of the widget.
        
        Keywords:
            x x coordinate of the mouse.
            y y coordinate of the mouse.
            width width of the window.
            height height of the window.
            
        Return:
            Pair of relative coordinates bounded between -1 and +1.
        """
        rel_x = (x - self.width / 2) / (self.width / 2)
        if rel_x > 1:
            rel_x = 1
        elif rel_x < -1:
            rel_x = -1
            
        rel_y = (self.height / 2 - y) / (self.height / 2)
        if rel_y > 1:
            rel_y = 1
        elif rel_y < -1:
            rel_y = -1  

        return rel_x, rel_y
