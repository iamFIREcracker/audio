#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import gobject

import audio.source
import audio.visual


def delete_cb(visualizer, event, source, loop):
    source.stop()
    loop.quit()

def new_data_cb(source, data, visualizer):
    visualizer.refresh(data)
    
def main(argv):
    if len(argv) < 2:
        print "Usage: {0} <source> [<options> ..]".format(sys.argv[0])
        return 1
    
    loop = gobject.MainLoop()
    
    if '--analyzer' in argv:
        visualizer = audio.visual.Analyzer()
    else:
        visualizer = audio.visual.Oscilloscope('--fill' in argv)
        
    if argv[1] == 'mic':
        source = audio.source.Microphone(emit=True)
    elif argv[1] == 'tone':
        source = audio.source.Tone(emit=True)
    else:
        location = argv[1]
        if not location.startswith('/'):
            location = os.path.join(os.getcwd(), location)
        source = audio.source.AudioFile(location, emit=True)
        
    visualizer.connect('delete-event', delete_cb, source, loop)
    source.connect('new-data', new_data_cb, visualizer)
    source.start()
    
    gobject.threads_init()
    loop.run()
    
    return 0
    
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
