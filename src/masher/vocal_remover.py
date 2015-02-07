# Author: Kevin Zheng
# Created: 2/7/15

import echonest.remix.audio as audio
import echonest.remix.modify as modify
import numpy as np


def remove_vocals(song):
    '''give it a AudioData file, it'll return one w/ vocals removed'''
    if not issubclass(song.__class__, audio.AudioData):
        print 'Got %s, expected AudioData' % type(song)
        raise TypeError
    # new array of same size
    out_shape = (len(song.data),)
    bg_only = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
    # iterate though old song
    idx_0 = None
    count = 0
    assign = 0
    print len(song.data)
    for x in np.nditer(song.data):
        if count % 2 == 1:
            new = np.subtract(np.divide(idx_0, 2), np.divide(x, 2))
            bg_only.data[assign] = new
            assign += 1
        else:
            idx_0 = x
        count += 1
        if count % 100000 == 0:
            print count
    return bg_only