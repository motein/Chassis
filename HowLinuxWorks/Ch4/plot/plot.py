#!/usr/bin/python3

import numpy as np
from PIL import Image
import matplotlib
import os
import sys

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import rcParams

plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "TakaoPGothic"

def plot_sched(concurrency):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(concurrency):
        x, y = np.loadtxt("{}.data".format(i), unpack=True)
        ax.scatter(x,y,s=1)
    ax.set_title("visualization of time slices (degree of parallelism={})".format(concurrency))
    ax.set_xlabel("elapsed time[ms]")
    ax.set_xlim(0)
    ax.set_ylabel("progress[%]")
    ax.set_ylim([0,100])
    legend = []
    for i in range(concurrency):
        legend.append("load handling"+str(i))
    ax.legend(legend)

    pngfilename = "sched-{}.png".format(concurrency)
    jpgfilename = "sched-{}.jpg".format(concurrency)
    fig.savefig(pngfilename)
    img = Image.open(pngfilename).convert("RGB").save(jpgfilename)
    os.remove(pngfilename)