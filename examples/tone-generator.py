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
    if __debug__:
        print 'dnd-value', x, y
    source.set_values(x, y)

def main(argv):
    mainloop = gobject.MainLoop()

    window = gtk.Window()
    hbox = gtk.HBox()

    source = audio.source.Tone(emit=True)
    pad = audio.tool.Pad()
    hbox.pack_start(pad)
    if '--analyzer' in argv:
        visualizer = audio.visual.Analyzer()
        source.connect('new-data', new_data_cb, visualizer)
        hbox.pack_start(visualizer)
        window.set_default_size(500, 200)

    window.connect('delete-event', delete_cb, source, mainloop)
    pad.connect('delete-event', delete_cb, source, mainloop)
    pad.connect('end-dnd', end_dnd_cb, source)
    pad.connect('start-dnd', start_dnd_cb, source)
    pad.connect('dnd-value', dnd_value_cb, source)

    window.add(hbox)
    window.show_all()

    gobject.threads_init()
    mainloop.run()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
