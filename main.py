import fire
import pyaudio
import pdir
import numpy as np
import queue
import signal
from pdb import set_trace as st
from itertools import count
from lib.helpers import *
from lib.sig_handle import *


def pitch_shift_one_chunk(chunk, shift_amnt):
    freqs = np.fft.fft(chunk)
    shifted_freqs = np.roll(freqs, shift_amnt)
    shifted_freqs[0: shift_amnt] = 0
    chunk = np.fft.ifft(shifted_freqs).astype(np.int16)
    return chunk


def pitch_shift(int_data, d):
    # if not d.pitch_shift: return int_data
    chunks = 2
    shift_amnt = d.pitch_shift//chunks
    #chunk_size = int_data.size//chunks
    chunked_data = np.split(int_data, chunks)
    out_dta = np.array([], dtype=np.int16)
    for chunk in chunked_data:
        shifted_chunk = pitch_shift_one_chunk(chunk, shift_amnt)
        out_dta = np.concatenate([out_dta, shifted_chunk])
    return out_dta


def collect_audio_and_do_stuff(old_snd_dtas, strms, i, d):
    snd = Box(raw_data = strms.into.read(d.chunk))
    snd.int_data = np.fromstring(snd.raw_data, dtype=np.int16)
    print(sum(np.absolute(snd.int_data)))
    munged_data = (snd.int_data) * 2
    munged_data = pitch_shift(munged_data, d)
    strms.out.write(munged_data.tobytes())
    return old_snd_dtas + [snd]


def main(plot=False, write_wav=False, pitch_shift=False):
    d = make_blob(plot, pitch_shift)  # d = blob of rate&chunk axis&figure plot
    strms = make_streams(d)
    setup_sig_handler(strms)
    snd_dtas = []  # array of snd objects which each hold raw_data and int_data
    dta_list = np.array([1], dtype=np.int16)
    for i in count():
        snd_dtas = collect_audio_and_do_stuff(snd_dtas, strms, i, d)
        snd_dtas = plot_if_possible(snd_dtas, d)
        dta_list = write_file_try("test.wav", 20000, dta_list, snd_dtas, write_wav)


if __name__=="__main__":
    fire.Fire(main)
