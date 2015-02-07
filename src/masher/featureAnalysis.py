#get comparison metrics
import echonest.remix.audio as audio
import numpy as np
#loudness metric
def loudnessMetric(file1):
	song1 = audio.LocalAudioFile(file1)
	chunks1 = song1.analysis.segments
	gradient = []
	for i in xrange(len(chunks1)-1):
		dif = chunks1[i+1].mean_loudness() - chunks1[i].mean_loudness()
		time = chunks[i].duration
		gradient += [dif/time]
	assert(len(gradient) == len(chunks1)-1)
	return gradient

def loudnessCMP(file1,file2,threshold):
	gradient1 = loudnessMetric(file1)
	gradient2 = loudnessMetric(file2)
	#want them to align when they are 0

def pitchCmp(file1,file2,threshold):
	song1 = audio.LocalAudioFile(file1)
	song2 = audio.LocalAudioFile(file2)
	chunks1 = song1.analysis.segments
	chunks2 = song2.analysis.segments
	closeVals = []
	for i in xrange(len(chunks1)):
		for j in xrange(len(chunks2)):
			vec1 = np.array(chunks1[i])
			vec1 /= (np.dot(vec1,vec1)**0.5)
			vec2 = np.array(chunks2[j])
			vec2 /= (np.dot(vec2,vec2)**0.5)
			result = np.dot(vec1,vec2)
			if result >= threshold: closeVals += [(i,j,result)]
	return closeVals




