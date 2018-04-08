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


def soundplot(olddata, strms, i, d):
    snd = Box(raw_data = strms.into.read(d.chunk))
    snd.int_data = np.fromstring(snd.raw_data, dtype=np.int16)
    print(sum(np.absolute(snd.int_data)))
    silly_data = (snd.int_data) * 2
    strms.out.write(silly_data.tobytes())
    if len(olddata) >= 8:
        plt_dta = np.concatenate([x.int_data for x in olddata])
        if d.plot:
            plot_it(d.ax, d.fig, plt_dta)
        olddata = olddata[1:]
    return olddata + [snd]


def main(plot=False, write_wav=False):
    d = make_blob(plot)  # d = blob of rate&chunk axis&figure plot
    strms = make_streams(d)
    snd_datas = []  # array of snd objects which each hold raw_data and int_data
    dataCollection = np.array([1], dtype=np.int16)
    setup_sig_handler(strms)
    for i in count():
        snd_datas = soundplot(snd_datas, strms, i, d)
        if write_wav:
            dataCollection = writeFile("test.wav", 20000, dataCollection, snd_datas)


if __name__=="__main__":
    fire.Fire(main)
