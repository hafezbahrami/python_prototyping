"""
Let's assume we want to plot a certain data, which happened showing how Threads in Python perform the jobs, but one at the a time. meaning 
there is no paralelization. Every single task at each time involves one single process.
"""

import os
import pandas as pd
import time
from tqdm import tqdm as tqdm
import numpy as np
import matplotlib.pyplot as plt

# global style parameters, suc has background, .... 
plt.style.use('dark_background')
plt.rcParams['font.size'] = 16


if __name__ == "__main__":
    # Load data: This DataFrame data has 2 index: Time and Thread  ==> 2 columns of data in this DF is: "fn calls" and "activity"
    # how to read this DF: During time-spend in this Thread XX, how many function calls being made for this thread XX. For instance 
    # between time 0 to 50000 mili-sec, how many function calls being made by Thread #1. In the # of fn calls, for any Thread XX, at 
    # any time interval is non-zero, we mark the "Activity column" as True.
    data_path = os.path.join(os.path.dirname(__file__), "data_to_plot.pkl")
    data = pd.read_pickle(data_path)
    data = data.reset_index().drop(labels=[
        "module", "total threads"], axis=1).set_index(["thread", "time (ns)"])
    data.sort_index(inplace=True)
    data.loc[:, "Activity"] = data.loc[:, "fn calls"] > 0

    # Plot params
    NROWS = 3  # each frame has 3 horizontal plot
    NFRAMES_START = 0 # strat from Frame-0
    NFRAMES_STOP = 20 # 3600 , end at Frame_XX
    NFRAMES_TOTAL = 20 # 3600 # of total frames

    # Useful quantities
    NTHREADS = data.index.levels[0].size # as noted above, we have 2 indeexs for this DataFrame. Level-0 refers to Thread-#

    # get time data
    t = data.index.levels[1].unique()   # # as noted above, we have 2 indeexs for this DataFrame. Level-1 refers to Thread-#
    dt = t[1] - t[0]

    # split time into (probably 3) suitable chunks, corresponding to the time in horizontal axess of 3 sub-horizontal-plots in one frame
    t_lims = [(i*t[-1]/NROWS, (i+1)*t[-1]/NROWS)
              for i in range(0, NROWS)]

    timer0 = time.perf_counter()
    
    # Loop over whatever # of frames we want to creat   ==>   Frame0, Frame1, Frame2, ....
    for frame in tqdm(range(NFRAMES_START, NFRAMES_STOP), leave=False, desc="frame"):  # animation frames
        t_curr = t[-1]*frame/(NFRAMES_TOTAL-1)  # current time to plot upto

        # create the plot. Create a plot, with 3 horizontal sub-plot in it
        fig, axs = plt.subplots(figsize=(16, 8), nrows=NROWS,
                                constrained_layout=True, sharey=True)
        fig.suptitle(f"t = {t_curr/1E6:.0f} ms")# to remove 6 zros of a mili-sec time-scale

        for ax, t_lim in zip(axs, t_lims):  # loop over each axis (each 3 horizontal subplots)

            for thread, df0 in data.groupby("thread"):  # loop over each thread
                df0 = df0.loc[thread] # for this specific Thread (# XX), get the corresponding DF with 3 columns: "time (ms)", "fn calss", "Activity"
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

    timer1 = time.perf_counter()
    NFRAMES = NFRAMES_STOP-NFRAMES_START
    deltat = timer1-timer0
    print(
        f"\nGenerated {NFRAMES} frames in {deltat:.1f} "
        f"seconds ({NFRAMES/deltat:.1f} FPS)")
