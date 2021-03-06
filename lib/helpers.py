import pyaudio
import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
from box import Box


def plot_if_possible(old_snd_dtas, d):
    if len(old_snd_dtas) >= 8:
        plt_dta = np.concatenate([x.int_data for x in old_snd_dtas])
        if d.plot:
            plot_it(d.ax, d.fig, plt_dta)
        old_snd_dtas = old_snd_dtas[1:]
    return old_snd_dtas


def make_streams(d):
    s = Box()
    s.into = make_input(d)
    s.out = make_output(d)
    return s


def make_input(d):
    p = pyaudio.PyAudio()
    return p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=d.rate,
        input=True,
        frames_per_buffer=d.chunk)


def make_output(d):
    p = pyaudio.PyAudio()
    return p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=d.rate,
        output=True,
        frames_per_buffer=d.chunk)


def close_streams(streams):
    for stream in streams:
        stream.stop_stream()
        stream.close()


def plot_it(ax, fig, plt_dta):
    ax.clear()
    ax.set_ylim([-30000,30000])
    ax.plot(plt_dta)
    fig.canvas.draw()


def set_up_ax_fig():
    fig = plt.figure()
    fig.show()
    fig.canvas.draw()
    ax = fig.add_subplot(111)
    ax.set_ylim([-30000,30000])
    return ax, fig


def make_blob(plot, pitch_shift):
    d = Box()  # d = blob of rate&chunk axis&figure
    d.pitch_shift = pitch_shift
    d.rate = 44100
    d.chunks_per_second = 1
    d.chunk = int(d.rate/d.chunks_per_second)  # d.rate / number of updates per second
    d.plot = plot
    if plot:
        d.ax, d.fig = set_up_ax_fig()
    return d


def write_file_try(filename, rate, nparray, dataStream, write_wav):
    if not write_wav: return
    scipy.io.wavfile.write(filename, rate, nparray)
    return np.append(nparray, dataStream[-1].data)
