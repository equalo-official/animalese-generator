import os
import random
import re
import string
from pydub import AudioSegment, playback


class AnimaleseGenerator(object):
    ALL_CHARS = list(string.ascii_lowercase + 'ST P')  # lower alpha, special, and punctuation sounds
    ENUM_MAP = {char: idx for idx, char in
                enumerate(ALL_CHARS, start=1)}  # character/index relationship: for accessing char filenames
    RE_INVALID = re.compile(r'([^a-z .,?!])')  # re method: for invalid character replacements
    RE_SPECIAL = re.compile(r'([st]h)')  # re method: for special sounds
    RE_REPEAT = re.compile(r'(.)\1+')  # re method: for repeated characters
    RE_SEGMENT = re.compile(r'([^.?! ].*?[.?!])')  # re method: for segmenting sentences
    RE_PUNCTUATION = re.compile(r'[?,.!]')

    @classmethod
    def _filename(cls, pitch, char):
        filename = os.path.join(os.curdir,
                                'sounds',
                                pitch,
                                f'sound{cls.ENUM_MAP[char]:02d}.wav')
        return filename

    @classmethod
    def _clean(cls, speech):
        if not isinstance(speech, str):
            message = f'Speech must be of type `str.`'
            raise TypeError(message)

        def special_replace(matchobj):  # For remapping 'th' and 'sh' to 'T' and 'S'
            return 'S' if matchobj.group(1) == 'sh' else 'T'

        speech = speech.lower()  # Forces letter characters to lowercase
        speech = cls.RE_INVALID.sub('', speech)  # removes invalid characters
        speech = cls.RE_SPECIAL.sub(special_replace, speech)  # replaces special sounds
        speech = cls.RE_REPEAT.sub(r'\1', speech)  # removes repeated characters
        speech = cls.RE_PUNCTUATION.sub('P', speech)  # replaces punctuation characters
        return speech

    @classmethod
    def _segment(cls, speech):
        sentences = []
        num_chars = len(speech)
        endspan = 0

        matchobjs = cls.RE_SEGMENT.finditer(speech)
        for matchobj in matchobjs:
            _, endspan = matchobj.span()
            sentence = matchobj.group()
            sentences.append(sentence)

        if endspan < num_chars:  # catch for strings that end without punctuation
            unmatched_sentence = speech[endspan:]
            sentences.append(unmatched_sentence)

        return sentences

    @classmethod
    def _octaves(cls, speech, pitch, isquestion=False):
        num_chars = len(speech)
        rnd_factor = 0.35 if pitch == 'med' else 0.25
        if isquestion:
            octaves = [2.0 + random.random() * rnd_factor +
                       (index >= 0.8 * num_chars) * (0.02 * index + 0.1) for index in range(num_chars)]
        else:
            octaves = [2.3 + random.random() * rnd_factor for _ in range(num_chars)]
        return octaves

    @classmethod
    def _audio(cls, speech, octaves, pitch):
        audio_segment = AudioSegment.empty()
        for char, octave in zip(speech, octaves):
            char_filename = cls._filename(pitch, char)
            char_sound = AudioSegment.from_wav(char_filename)
            sample_rate = int(char_sound.frame_rate * (2.0 ** octave))
            char_sound = char_sound._spawn(char_sound.raw_data, overrides={'frame_rate': sample_rate})
            char_sound = char_sound.set_frame_rate(44100)
            audio_segment += char_sound

        return audio_segment

    @classmethod
    def make(cls, speech, pitch='med'):
        """
        Method for delivering speech. Octave shifts are handled automatically for each sentence.
        :param speech: One or more sentences to be digested
        :param pitch: 'lowest', 'low', 'med', or 'high'

        Future improvements:
            Fix issues with abbreviations, e.g. 'Mr.', 'Sr.', and 'Dr..' and so on.
                Perhaps a regex filter with the common ones could be added.
        """
        audio_segment = AudioSegment.empty()
        sentences = cls._segment(speech)
        for sentence in sentences:
            isquestion = sentence[-1] == '?'
            sentence = cls._clean(sentence)
            octaves = cls._octaves(sentence, pitch, isquestion)
            audio_subsegment = cls._audio(sentence, octaves, pitch)
            audio_segment += audio_subsegment

        return audio_segment


# Usage
if __name__ == '__main__':
    stringy = ("We use words like honor, code, loyalty...we use these words "
               "as the backbone to a life spent defending something. You use 'em as a "
               "punchline. I have neither the time nor the inclination to explain myself "
               "to a man who rises and sleeps under the blanket of the very freedom I "
               "provide, then questions the manner in which I provide it! I'd rather you "
               "just said thank you and went on your way. Otherwise, I suggest you pick up"
               "a weapon and stand a post. Either way, I don't give a damn what you think "
               "you're entitled to!")

    pitch = 'low'  # choose between 'high', 'med', 'low', or 'lowest'
    audio_segment = AnimaleseGenerator.make(stringy, pitch)
    
#   Playback (requires ffmpeg or libav)
#    playback.play(audio_segment)

#   Export: 
    export_dir = os.path.join(os.curdir, 'sound.wav')
    audio_segment.export(export_dir, 'wav')
