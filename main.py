import fire
import pyaudio
import pdir
import numpy as np
from pdb import set_trace as st
from box import Box
from itertools import count, chain
from helpers import *


def soundplot(olddata, stream, out_stream, i, d):
    snd = Box()
    snd.raw_data = stream.read(d.chunk)
    snd.data = np.fromstring(snd.raw_data, dtype=np.int16)
    print(sum(np.absolute(snd.data)))
    # out_stream.write(olddata)
    if len(olddata) >= 8:
        plt_dta = np.concatenate([x.data for x in olddata])
        plot_it(d.ax, d.fig, plt_dta)
        olddata = olddata[1:]
    return olddata + [snd]

if __name__=="__main__":
    d = Box()  # d = blob of rate&chunk axis&figure
    d.rate = 4410  # 44100
    d.chunk = int(d.rate/8)  # d.rate / number of updates per second
    d.ax, d.fig = set_up_ax_fig()

    stream = make_input(d)
    out_stream = make_output(d)
    #d.rate = 44100
    data = []
    for i in count():
        data = soundplot(data, stream, out_stream, i, d)
    close_streams([stream, out_stream])
