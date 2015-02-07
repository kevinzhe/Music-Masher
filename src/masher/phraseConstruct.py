import echonest.remix.audio as audio
import numpy as np
import featureAnalysis

def phraseConstruct(file1,file2):
	song1 = audio.LocalAudioFile(file1)
	song2 = audio.LocalAudioFile(file2)
	matchup = featureAnalysis.main(song1,song2)
	print matchup

phraseConstruct("dhorse1.wav","clock1.wav")
