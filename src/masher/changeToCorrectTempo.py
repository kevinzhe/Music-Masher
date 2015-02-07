import echonest.remix.audio as audio
import math
import os
import sys
# Import the timestretching library.  
import dirac
from echonest.remix import audio

#file1 = audio.LocalAudioFile("partyusa.mp3")

def changeToCorrectTempo(audioFile, targetTempo):
    #takes in an audioFile, targetTempo, returns audioFile @ correct tempo
    currentTempo = audioFile.analysis.tempo['value']
    bars = audioFile.analysis.bars
    collect = []

    # This loop streches each beat by a varying ratio, and then re-assmbles them.
    for bar in bars:
        # Get the beats in the bar
        beats = bar.children()
        for beat in beats:
            # Note that dirac can't compress by less than 0.5!

            ratio = currentTempo/targetTempo
            #formula for changing currentTempo to targetTempo
            
            # Get the raw audio data from the beat and scale it by the ratio
            # dirac only works on raw data, and only takes floating-point ratios
            beat_audio = beat.render()
            scaled_beat = dirac.timeScale(beat_audio.data, ratio)
            # Create a new AudioData object from the scaled data
            ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape, 
                            sampleRate=audioFile.sampleRate, numChannels=scaled_beat.shape[1])
            # Append the new data to the output list!
            collect.append(ts)

    # Assemble and write the output data
    output = audio.assemble(collect, numChannels=2)
    return output

#changeToCorrectTempo(file1,120.055).encode("TestOutput.mp3")
