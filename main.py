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


def collect_audio_and_do_stuff(old_snd_dtas, strms, i, d):
    snd = Box(raw_data = strms.into.read(d.chunk))
    snd.int_data = np.fromstring(snd.raw_data, dtype=np.int16)
    print(sum(np.absolute(snd.int_data)))
    silly_data = (snd.int_data) * 2
    strms.out.write(silly_data.tobytes())
    return old_snd_dtas + [snd]


def main(plot=False, write_wav=False):
    d = make_blob(plot)  # d = blob of rate&chunk axis&figure plot
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
