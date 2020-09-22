import random
from pydub import AudioSegment
from pydub.playback import play

stringy = '*i a*r shi*k !f doi*m zi*s'
pitch = 'BOY' # choose between 'high', 'med', 'low', or 'lowest', or 'BOY', 'GAL' or 'MAN'
kanamode = True #should be true if using 'BOY', 'GAL' or 'MAN' - stringy should only use valid kana. Invalid Kana are user error.

stringy = stringy.lower()
sounds = {}

if kanamode:
    keys = ['a','i','u','e','o','ka','ki','ku','ke','ko','sa','shi','su','se','so','ta','chi','tsu','te','to','na','ni','nu','ne','no','ha','hi','hu','he','ho','ma','mi','mu','me','mo','ya','yu','yo','ra','ri','ru','re','ro','wa','wo','n','ga','gi','gu','ge','go','za','ji','zu','ze','zo','da','dzi','dzu','de','do','ba','bi','bu','be','bo','pa','pi','pu','pe','po','*0','*1','*2','*3','*4','*5','*6','*7','*8','*9','!a','!b','!c','!d','!e','!f','!g','!h','!i','!j','!k','!l','!m','!n','!o','!p','!q','!r','!s','!t','!u','!v','!w','!x','!y','!z','*i','*r','*s','*b','*i','*f','*a','*m','*n','*f','*g','*k','*z','*o','*q','*u','*d','*v']
    if pitch == 'BOY':
        indexnum = 219
    elif pitch == 'GAL':
        indexnum = 344
    else:
        indexnum = 469
    for index,ltr in enumerate(keys):
        num = index+indexnum
        sounds[ltr] = './sounds/'+pitch+'/00'+str(num)+' - WAV_'+str(num)+'_GUESS_BANK_SE_DOUBUTSUGO_'+pitch+'.wav'
else:
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

if kanamode:
    for i, char in enumerate(stringy):
        try:
            if char=='n' and stringy[i+1] not in ['a','i','u','e','o']: # n kana
                infiles.append(sounds[char])
                continue
            elif char in ['a','i','u','e','o']: #don't duplicate vowels
                if stringy[i-1] in ['a','i','u','e','o',' ','^','.','?',',']:
                    infiles.append(sounds[char])
                continue
            elif char+stringy[i+1] in ['ch','sh','ts','dz']: #three-letter kana
                infiles.append(sounds[char+stringy[i+1]+stringy[i+2]])
                continue
            elif stringy[i-1]+char in ['ch','sh','ts','dz']: #don't dupe three-letter kana
                continue
            elif char == ',' or char == '?':
                infiles.append(sounds['.'])
                continue
            elif char in ['!','*']: #A-Z keyboard sound, enunciation sounds
                infiles.append(sounds[char+stringy[i+1]])
                continue
            elif stringy[i-1] in ['!','*']: 
                continue
            elif char == stringy[i-1]: #skip repeat letters
                continue
        except:
            pass
        if not char.isalpha() and char != '.' and i+1>=len(stringy): # skip characters that are not letters or periods. 
            infiles.append(sounds[char+stringy[i+1]])
else:
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

if kanamode:
    shiftpitch = 0
else:
    shiftpitch = 2

print(len(infiles))
for index,sound in enumerate(infiles):
	tempsound = AudioSegment.from_wav(sound)
	if stringy[len(stringy)-1] == '?':
		if index >= len(infiles)*.8:
			octaves = random.random() * rnd_factor + (index-index*.8) * .1 + shiftpitch + 0.1 # shift the pitch up by half an octave (speed will increase proportionally)
		else:
			octaves = random.random() * rnd_factor + shiftpitch
	else:
		octaves = random.random() * rnd_factor + shiftpitch + 0.3 # shift the pitch up by half an octave (speed will increase proportionally)
	new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
	new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
	new_sound = new_sound.set_frame_rate(44100) # set uniform sample rate
	combined_sounds = new_sound if combined_sounds is None else combined_sounds + new_sound


combined_sounds.export("./sound.wav", format="wav")
