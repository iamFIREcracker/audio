#!/usr/bin/python
# -*- coding: Latin-1 -*-

"""Module containing audio sources.
"""

from __future__ import division
from struct import unpack

import gobject
import gst


class Source(gobject.GObject):
    """Base audio source object.
    """
    
    """Signal emitted when a new audio buffer is ready for processing.
    """
    __gsignals__ = {
            'new-data': (gobject.SIGNAL_RUN_FIRST, None,
                         (gobject.TYPE_PYOBJECT,)),
    }
    
    def __init__(self, pipeline, speakers, emit):
        """Constructor.
        
        Keywords:
            pipeline string representing a gstreamer pipeline.
            speakers flag indicating wether to output data to the speakers.
            emit flag indicating wether to emit signals notifying new data.
        """
        super(Source, self).__init__()
        
        self.pipeline = gst.parse_launch(pipeline)
        if not speakers:
            self.pipeline.get_by_name('asink').set_state(gst.STATE_NULL)
        if emit:
            self.pipeline.get_by_name('fsink').connect('handoff',
                                                       self.handoff_cb)
            
    def handoff_cb(self, fakesink, buff, pad):
        """Invoked when the fakesink collected a new buffer of data.
        
        The format of the input buffer is supposed to be:
            channels: mono
            samplerate: 44100
            bitspersample: 16 signed
            endianess: little
            
        Emit a signal containing the array of data, normalized between -1 and
        +1.
        """
        samples = buff.size // 2

        fmt = "<" + str(samples) + "h"
        data = [v / 32768 for v in unpack(fmt, buff.data)]
        
        self.emit('new-data', data)
    
    def start(self):
        """Start the pipeline.
        """
        self.pipeline.set_state(gst.STATE_PLAYING)

    def pause(self):
        """Pause the pipeline.
        """
        self.pipeline.set_state(gst.STATE_READY)

    def stop(self):
        """Stop the pipeline.
        """
        self.pipeline.set_state(gst.STATE_READY)


class Microphone(Source):
    """Microphone source object.
    """
    
    def __init__(self, speakers=True, emit=False):
        """Constructor.
        
        Keywords:
            speakers flag indicating wether to output data to the speakers.
            emit flag indicating wether to emit signals notifying new data.
        """
        super(Microphone, self).__init__(
            '''alsasrc name=source !
               audioconvert !
               audio/x-raw-int,
                       channels=1,
                       rate=44100,
                       width=16,
                       signed=true,
                       endianness=1234 !
               tee name=t !
               queue !
                   fakesink name=fsink signal-handoffs=true sync=true t. !
               queue !
                   autoaudiosink name=asink''', speakers, emit)


class Tone(Source):
    """Single tone source object.
    """
    
    def __init__(self, speakers=True, emit=False):
        """Constructor.
        
        Keywords:
            speakers flag indicating wether to output data to the speakers.
            emit flag indicating wether to emit signals notifying new data.
        """
        super(Tone, self).__init__(
            '''audiotestsrc name=source !
               audioconvert !
               audio/x-raw-int,
                       channels=1,
                       rate=44100,
                       width=16,
                       signed=true,
                       endianness=1234 !
               tee name=t !
               queue !
                   fakesink name=fsink signal-handoffs=true sync=true t. !
               queue !
                   autoaudiosink name=asink''', speakers, emit)
        
    def set_values(self, freq, volume):
        """Set source properties.
        
        Keywords:
            freq new frequency value.
            volume new volume value.
        """
        source = self.pipeline.get_by_name('source')
        source.set_property('freq', max(0, min(freq, 20000)))
        source.set_property('volume', max(0, min(volume, 1)))


class AudioFile(Source):
    """Audio file source object.
    """
                 
    
    def __init__(self, location, speakers=True, emit=False):
        """Constructor.
        
        Keywords:
            location location of the file to play
            speakers flag indicating wether to output data to the speakers.
            emit flag indicating wether to emit signals notifying new data.
        """
        super(AudioFile, self).__init__(
            '''filesrc location={0} !
               decodebin !
               audioconvert !
               audio/x-raw-int,
                       channels=1,
                       rate=44100,
                       width=16,
                       signed=true,
                       endianness=1234 !
               tee name=t !
               queue !
                   fakesink name=fsink signal-handoffs=true sync=true t. !
               queue !
                   autoaudiosink name=asink'''.format(location), 
            speakers, emit)