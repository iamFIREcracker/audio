#!/usr/bin/python
# -*- coding: Latin-1 -*-

"""Test script for the audio module.

Create an audio source depending on the command line argument provided and
start to visualize the audio shape on screen.
"""

import os
import sys

import gobject
import gtk

import audio


def delete_cb(visualizer, event, source):
    """Invoked when the visualizer window is closed.
    
    Stop the source, then quit the gtk mainloop.
    """
    source.stop()
    gtk.main_quit()

def new_data_cb(source, data, visualizer):
    """Invoked when the audio source has produced new audio data.
    
    Call a refresh of the visualizer canvas.
    """
    visualizer.refresh(data)
    
def main(argv):
    if len(argv) != 2:
        print "Usage: {0} <source>".format(sys.argv[0])
        return 1
    
    visualizer = audio.visual.Analyzer()
    
    if argv[1] == 'mic':
        source = audio.source.Microphone(emit=True)
    elif argv[1] == 'tone':
        source = audio.source.Tone(emit=True)
    else:
        location = argv[1]
        if not location.startswith('/'):
            location = os.path.join(os.getcwd(), location)
        source = audio.source.AudioFile(location, emit=True)
        
    visualizer.connect('delete-event', delete_cb, source)
    source.connect('new-data', new_data_cb, visualizer)
    source.start()
    
    gobject.threads_init()
    gtk.main()
    
    return 0
    
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))