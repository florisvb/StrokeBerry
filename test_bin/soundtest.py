import pygame as pg
import numpy as np
import time


def_length = 1.0 / 24.0
log440 = np.log2(440.0)                


def GenerateTone( freq=440.0, vol=1.0, wave='sine', random=False,
                  length=def_length, vL=1, vR=1):
    """ GenerateTone( freq=440.0, vol=1.0, wave='sine', random=False,
                      length=(1.0 / 24.0) ) -> pygame.mixer.Sound

        freq:  frequency in Hz; can be passed in as an int, float,
               or string (with optional trailing octave, defaulting to 4):
               'A4' (440 Hz), 'B#', 'Gb-1'
        vol:  relative volume of returned sound; will be clipped
              into range 0.0 -> 1.0
        wave:  int designating waveform returned;
               one of 'sine', 'saw', or 'square'
        random:  boolean value; if True will modulate frequency randomly
        length:  relative length of the Sound returned;
                 bigger values will result in more longer and more accurate
                 waveforms, but will also take longer to create;
                 the default value should be adequate for most uses
    """

    (pb_freq, pb_bits, pb_chns) = pg.mixer.get_init()
    if type(freq) == str:
        i = 0
        while i < len(freq) and freq[i] not in '1234567890-':
            i += 1
        if i == 0:
            note = 'a'
        else:
            note = freq[: i].lower()
        if i == len(freq):
            octave = 4
        else:
            octave = int(freq[i: ])
        freq = 2.0 ** (log440 + notes_dct[note] / 12.0 + octave - 4)
    vol = np.clip(vol, 0.0, 1.0)

    if random:
        # Modulate frequency randomly, playing in previous mode selected.
        freq += (np.random.rand() * 2.0 - 1.0) * freq / 8.0
    multiplier = int(freq * length)
    length = max(1, int(float(pb_freq) / freq * multiplier))
    lin = np.linspace(0.0, multiplier, length, endpoint=False)
    if wave == 'sine':
        ary = np.sin(lin * 2.0 * np.pi)
    elif wave == 'saw':
        ary = 2.0 * ((lin + 0.5) % 1.0) - 1.0
    elif wave == 'square':
        ary = np.zeros(length)
        ary[lin % 1.0 < 0.5] = 1.0
        ary[lin % 1.0 >= 0.5] = -1.0
    else:
        print "wave parameter should be one of 'sine', 'saw', or 'square'."
        return None

    # If mixer is in stereo mode, double up the array information for
    # each channel.
    if pb_chns == 2:
        ary = np.repeat(ary[..., np.newaxis], 2, axis=1)

    if pb_bits == 8:
	
	if pb_chns == 2:
		ary[:,0] *= vL
		ary[:,1] *= vR	

        snd_ary = ary * 127.0
        return pg.sndarray.make_sound(snd_ary.astype(np.uint8) + 128)

    elif pb_bits == -16:
        snd_ary = ary * vol * float((1 << 15) - 1)
        return pg.sndarray.make_sound(snd_ary.astype(np.int16))
    else:
        print "Sound playback resolution unsupported (either 8 or -16)."
        return None






pg.mixer.init(44100, 8, 2, 512)
main_chn = pg.mixer.Channel(0)



vol = 0
while True:
	frq = np.random.randint(10,700)
	vol += 0.01
	if vol > 1:
		vol = 0
	sound = GenerateTone(440, vol, wave='sine', length=1/30., vL=vol, vR=1)
	
	if not main_chn.get_busy():
		main_chn.play(sound)
	else:
		main_chn.queue(sound)
	#main_chn.queue(sound)
	time.sleep(1/40.)