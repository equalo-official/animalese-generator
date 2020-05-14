import random
from pydub import AudioSegment
from pydub.playback import play

stringy = 'Oh me. Im not much of a traveler. I may have had a run in with a train in the past. But I got tired of chasing trains. Finally realized that the best way to catch one is to catch a ride on one. But I digress.'
pitch = 'low' # choose between 'high', 'med', 'low', or 'lowest'

stringy = stringy.lower()
sounds = {}

keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','th','sh',' ','.']
for index,ltr in enumerate(keys):
	num = index+1
	if num < 10:
		num = '0'+str(num)
	sounds[ltr] = './sounds/'+pitch+'/sound'+str(num)+'.wav'


infiles = []

#
for i, char in enumerate(stringy):
	try:
		if char == 's' and stringy[i+1] == 'h': #test for 'sh' sound
			infiles.append(sounds['sh'])
			continue
		elif char == 't' and stringy[i+1] == 'h': #test for 'th' sound
			infiles.append(sounds['th'])
			continue
		elif char == 'h' and (stringy[i-1] == 's' or stringy[i-1] == 't'): #test if previous letter was 's' or 's' and current letter is 'h'
			continue
		elif char == ',' or char == '?':
			infiles.append(sounds['.'])
			continue
		elif char == stringy[i-1]: #skip repeat letters
			continue
	except:
		pass
	if !char.isalpha() and char != '.': # skip characters that are not letters or periods. 
		continue
	infiles.append(sounds[char])

octaves = 2 # shift the pitch up by half an octave (speed will increase proportionally)
tempsound = AudioSegment.from_wav(infiles[0])
new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))

combined_sounds = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
combined_sounds = combined_sounds.set_frame_rate(44100) # set uniform sample rate

print(len(infiles))
for index,sound in enumerate(infiles):
	tempsound = AudioSegment.from_wav(sound)
	if stringy[len(stringy)-1] == '?':
		if index == len(infiles)*.85:
			octaves = random.random() * 0.35 + 2.0 # shift the pitch up by half an octave (speed will increase proportionally)
		else:
			octaves = random.random() * 0.35 + 1.8
	else:
		octaves = random.random() * 0.35 + 2.1 # shift the pitch up by half an octave (speed will increase proportionally)
	new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
	new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
	new_sound = new_sound.set_frame_rate(44100) # set uniform sample rate
	combined_sounds += new_sound


combined_sounds.export("./sound.wav", format="wav")
