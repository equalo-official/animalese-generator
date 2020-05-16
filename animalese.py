import random
from pydub import AudioSegment
from pydub.playback import play

stringy = 'The quick brown fox jumps over the lazy dog.'
pitch = 'med' # choose between 'high', 'med', 'low', or 'lowest'

stringy = stringy.lower()
sounds = {}

keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','th','sh',' ','.']
for index,ltr in enumerate(keys):
	num = index+1
	if num < 10:
		num = '0'+str(num)
	sounds[ltr] = './sounds/'+pitch+'/sound'+str(num)+'.wav'

if pitch == 'med':
	rnd_factor = .35
else:
	rnd_factor = .25

infiles = []

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
	if not char.isalpha() and char != '.': # skip characters that are not letters or periods. 
		continue
	infiles.append(sounds[char])

combined_sounds = None

print(len(infiles))
for index,sound in enumerate(infiles):
	tempsound = AudioSegment.from_wav(sound)
	if stringy[len(stringy)-1] == '?':
		if index >= len(infiles)*.8:
			octaves = random.random() * rnd_factor + (index-index*.8) * .1 + 2.1 # shift the pitch up by half an octave (speed will increase proportionally)
		else:
			octaves = random.random() * rnd_factor + 2.0
	else:
		octaves = random.random() * rnd_factor + 2.3 # shift the pitch up by half an octave (speed will increase proportionally)
	new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
	new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
	new_sound = new_sound.set_frame_rate(44100) # set uniform sample rate
	combined_sounds = new_sound if combined_sounds is None else combined_sounds + new_sound


combined_sounds.export("./sound.wav", format="wav")
