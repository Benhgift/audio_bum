import fire
import pyaudio
import pdir
import numpy as np
import queue
from pdb import set_trace as st
from itertools import count
from helpers import *


def soundplot(olddata, stream, out_stream, i, d):
    snd = Box()
    snd.raw_data = stream.read(d.chunk)
    snd.data = np.fromstring(snd.raw_data, dtype=np.int16)
    print(sum(np.absolute(snd.data)))
    silly_data = (snd.data) * 2
    out_stream.write(silly_data.tobytes())
    if len(olddata) >= 8:
        plt_dta = np.concatenate([x.data for x in olddata])
        st()
        #plot_it(d.ax, d.fig, plt_dta)
        olddata = olddata[1:]
    return olddata + [snd]

if __name__=="__main__":
    d = make_blob()  # d = blob of rate&chunk axis&figure
    stream = make_input(d)
    out_stream = make_output(d)
    data = []
    for i in count():
        data = soundplot(data, stream, out_stream, i, d)
    close_streams([stream, out_stream])
