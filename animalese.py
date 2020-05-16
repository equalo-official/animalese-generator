import random
from pydub import AudioSegment
from pydub.playback import play
from string import ascii_lowercase

stringy = 'The quick brown fox jumps over the lazy dog.'
pitch = 'med' # choose between 'high', 'med', 'low', or 'lowest'

stringy = stringy.lower()
sounds = {}

keys = [letter for letter in ascii_lowercase]
keys.extend(['th', 'sh', ' ', '.'])
for index, letter in enumerate(keys):
	num = index + 1
	if num < 10:
		num = f'0{num}'
	sounds[letter] = f'./sounds/{pitch}/sound{num}.wav'

if pitch == 'med':
	rnd_factor = 0.35
else:
	rnd_factor = 0.25

infiles = []

for i, char in enumerate(stringy):
	try:
		# Test for 'sh' sound
		if char == 's' and stringy[i + 1] == 'h':
			infiles.append(sounds['sh'])
			continue
		# Test for 'th' sound
		elif char == 't' and stringy[i + 1] == 'h':
			infiles.append(sounds['th'])
			continue
		# Test if previous letter was 's' or 's' and current letter is 'h'
		elif char == 'h' and (stringy[i - 1] == 's' or stringy[i - 1] == 't'):
			continue
		elif char == ',' or char == '?':
			infiles.append(sounds['.'])
			continue
		# Skip repeat letters
		elif char == stringy[i - 1]:
			continue
	except:
		pass
	# Skip characters that are not letters or periods.
	if not char.isalpha() and char != '.':
		continue
	infiles.append(sounds[char])

combined_sounds = None

print(len(infiles))
for index, sound in enumerate(infiles):
	tempsound = AudioSegment.from_wav(sound)
	if stringy[len(stringy) - 1] == '?':
		if index >= len(infiles) * 0.8:
			# Shift the pitch up by half an octave (speed will increase proportionally)
			octaves = random.random() * rnd_factor + (index - index * 0.8) * 0.1 + 2.1
		else:
			octaves = random.random() * rnd_factor + 2.0
	else:
		# Shift the pitch up by half an octave (speed will increase proportionally)
		octaves = random.random() * rnd_factor + 2.3
	new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
	new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
	# Set uniform sample rate
	new_sound = new_sound.set_frame_rate(44100)
	combined_sounds = new_sound if combined_sounds is None else combined_sounds + new_sound


combined_sounds.export("./sound.wav", format="wav")
