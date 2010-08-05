# -*- coding: Latin-1 -*-

import sys

import gobject

import audio.visual
import audio.source
import audio.tool


def delete_cb(window, event, source, mainloop):
    source.stop()
    mainloop.quit()

def end_dnd_cb(widget, source):
    source.pause()
    
def start_dnd_cb(widget, source):
    source.start()
    
def dnd_value_cb(widget, x, y, source):
    print 'dnd-value', x, y
    source.set_values(x, y)
    
def main():
    mainloop = gobject.MainLoop()
    source = audio.source.Tone()
    pad = audio.tool.Pad()

    pad.connect('delete-event', delete_cb, source, mainloop)
    pad.connect('end-dnd', end_dnd_cb, source)
    pad.connect('start-dnd', start_dnd_cb, source)
    pad.connect('dnd-value', dnd_value_cb, source)
    
    gobject.threads_init()
    mainloop.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())