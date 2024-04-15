"""Load in some data and create an activity plot animation.
The data was created using the threading module and provides histograms
of function calls vs time in nanoseconds for each thread.
This script uses multiple processes to hasten the workload"""

import pandas as pd
import time
import os
from multiprocessing import Pool
from tqdm import tqdm as tqdm
import numpy as np
import matplotlib.pyplot as plt

from typing import List, Tuple

plt.style.use('dark_background')
plt.rcParams['font.size'] = 16

# Look at the 00_animation_generation_single_process.py file for description on what we plot here
def plotter(data, N0, N1, NT = 3600):
    """We want to create total number of Frame of NT. 
    That starts from Frame-N0 and goes all the way to Frame-N1."""
    # Plot Params
    NROWS = 3

    # Useful quantities
    NTHREADS = data.index.levels[0].size

    # get time data
    t = data.index.levels[1].unique()

    # split time into suitable chunks
    t_lims = [(i*t[-1]/NROWS, (i+1)*t[-1]/NROWS)
              for i in range(0, NROWS)]

    for frame in range(N0, N1):  # animation frames
        t_curr = t[-1]*frame/(NT-1)  # current time to plot upto

        # create the plot
        fig, axs = plt.subplots(figsize=(16, 8), nrows=NROWS,
                                constrained_layout=True, sharey=True)
        fig.suptitle(f"t = {t_curr/1E6:.0f} ms")

        for ax, t_lim in zip(axs, t_lims):  # loop over each axis

            for thread, df0 in data.groupby("thread"):  # loop over each thread
                df0 = df0.loc[thread]
                _xy = df0.loc[t_lim[0]:t_lim[1], "Activity"]
                # just set the values to false that we don't plot
                _xy.loc[_xy.index > t_curr] = False
                _x = _xy.index.values/1E6
                _y = _xy.values
                # add red current line time
                if t_curr >= t_lim[0] and t_curr < t_lim[1]:
                    ax.axvline(x=t_curr/1E6, color="tab:red")
                if t_curr >= t_lim[0]:
                    ax.fill_between(
                        _x, thread, thread+_y, label=f"thread {thread}")

            # grid lines, limits, and ticks
            ax.grid(axis="y", alpha=0.1)
            ax.set_ylim([-0.1, NTHREADS+0.1])
            ax.set_yticks(np.arange(0, NTHREADS+1, 1))
            ax.set_yticklabels(
                np.arange(0, NTHREADS+1, 1, dtype=np.int64))
            ax.set_xlim(np.array(t_lim)/1E6)

        axs[-1].set(xlabel="time (ms)")

        # legend
        axs[0].legend(bbox_to_anchor=(0.5, 1),
                      ncol=8,
                      loc="lower center", fontsize=12)

        data_path = os.path.join(os.path.dirname(__file__), "frames")
        fig.savefig(
            f"{data_path}/frame_{frame:04.0f}.png", dpi=150)
        
        plt.close(fig)


if __name__ == "__main__":
    """We want to load data once, and then distribute the plotting-action into different processes"""

    NFRAMES_TOTAL = 200
    NPLOTTERS = os.cpu_count()

    # Load data
    data_path = os.path.join(os.path.dirname(__file__), "data_to_plot.pkl")
    data = pd.read_pickle(data_path)
    
    data = data.reset_index().drop(labels=[
        "module", "total threads"], axis=1).set_index(["thread", "time (ns)"])
    data.sort_index(inplace=True)
    data.loc[:, "Activity"] = data.loc[:, "fn calls"] > 0

    # (I) cretae XX number of processes
    with Pool(processes=NPLOTTERS) as p:
        time.sleep(1)

        # (II) create iterables: chunck of tasjs in a list, then we want to distribute this iterable to various processes.
        #      iterable is a list of tuples. In each Tuple we have:
        #                                ( DataFrame,  N_frame_start, N_frame_end, total_#_of_frame). 
        #      Basically the 3 last ints are ipot to the plot method above, that each process need to make a call.
        bounds = np.linspace(0, NFRAMES_TOTAL, NPLOTTERS+1, dtype=np.int64)
        iterable: List[Tuple[pd.DataFrame, int, int, int]] = [(data, bounds[i], bounds[i+1], NFRAMES_TOTAL)
                    for i in range(NPLOTTERS)]
        timer0 = time.perf_counter()

        # (III) Sending each individual task_of_plotting in the iterable, into various processes we cretaed using Pool library above
        p.starmap(plotter, iterable, chunksize=1)
        timer1 = time.perf_counter()

        deltat = timer1-timer0
        print(
            f"\nGenerated {NFRAMES_TOTAL} frames in {deltat:.1f} seconds"
            f" ({NFRAMES_TOTAL/deltat:.1f} FPS)")
