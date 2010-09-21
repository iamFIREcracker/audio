#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import gobject
import gtk

import audio.visual
import audio.source
import audio.tool


def delete_cb(window, event, source, mainloop):
    source.stop()
    mainloop.quit()

def new_data_cb(source, data, visualizer):
    visualizer.refresh(data)
    
def end_dnd_cb(widget, source):
    source.pause()
    
def start_dnd_cb(widget, source):
    source.start()
    
def dnd_value_cb(widget, x, y, source):
    print 'dnd-value', x, y
    source.set_values(x, y)

def main(argv):
    mainloop = gobject.MainLoop()
    window = gtk.Window()

    source = audio.source.Tone(emit=True)
    visualizer = audio.visual.Analyzer()
    pad = audio.tool.Pad()

    window.connect('delete-event', delete_cb, source, mainloop)
    source.connect('new-data', new_data_cb, visualizer)
    pad.connect('delete-event', delete_cb, source, mainloop)
    pad.connect('end-dnd', end_dnd_cb, source)
    pad.connect('start-dnd', start_dnd_cb, source)
    pad.connect('dnd-value', dnd_value_cb, source)
    
    window.add(visualizer)
    window.show_all()

    gobject.threads_init()
    mainloop.run()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
