import pyaudio
import matplotlib.pyplot as plt


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

def plot_it(ax, fig, plt_dta):
    ax.clear()
    ax.set_ylim([-30000,30000])
    ax.plot(plt_dta)
    fig.canvas.draw()

def set_up_ax_fig():
    plt.ion()
    fig = plt.figure()
    fig.show()
    fig.canvas.draw()
    ax = fig.add_subplot(111)
    ax.set_ylim([-30000,30000])
    return ax, fig
