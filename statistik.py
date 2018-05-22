import csv
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import pdb

import os

# read when I worked at what projects, shows some statistics
# plot over days/weeks/months: how much have i worked on each project / total
# plot over time: weighted average on what I worked
# day average: how much do i work on what

def read_statistic():

    dir_path = os.path.dirname(os.path.realpath(__file__))

    # creates a dict of changetimes, that contains for each project
    # a list of times where I changed the work status
    # first entry is a start time
    changetimes = {"total": []} # project -> list of timestamps
    working_on = None
    with open(os.path.join(dir_path, 'statistik.csv'), 'r') as file:
        reader = csv.reader(file, delimiter=",")
        for time_str, action, project in reader:
            time = datetime.strptime(time_str, "%m/%d/%y %H:%M:%S")

            if action == "start":
                # tell the other project I was working on that I stopped to work on that project
                if working_on is not None:
                    changetimes[working_on] = changetimes.get(working_on, []) + [time]
                else:
                    # new start time for total
                    changetimes["total"].append(time)

                # tell this project that I started working on it, unless I was working on it already
                if len(changetimes.get(project, [])) % 2 == 0: # last status on that project: I have not been working
                    working_on = project
                    changetimes[working_on] = changetimes.get(working_on, []) + [time]
            else:
                if working_on is not None:
                    changetimes[working_on].append(time)
                    changetimes["total"].append(time)
                working_on = None

    return changetimes


def plot_total(times, label, interval, start, end, ax):
    """
    times: list of timestamps,
        where even entries are start times
        and odd entries are end times
    label: what I worked on, eg uni
    interval: timespan, eg day, week or month
    start: timestamp where the plot starts
    ax: ax to plot on
    """
    curr_time = start
    per_interval = []
    while len(times) >=2 and curr_time < times[-1]:
        tmp = curr_time
        total = timedelta(0)

        while len(times) >=2 and tmp < curr_time + interval:
            t_start, t_stop, times = times[0], times[1], times[2:]
            total += t_stop - t_start
            tmp = t_stop
        per_interval.append(total)

        curr_time += interval

    while curr_time < end:
        per_interval.append(timedelta(0))
        curr_time += interval

    per_interval = [i.seconds for i in per_interval]
    ax.plot(range(len(per_interval)), per_interval, label=label)


def plot_average(changetimes, start):
    # plot over time: weighted average on what I worked
    pass


def plot_day_average(changetimes, start):
    # day average: how much do i work on what
    pass


dir_path = os.path.dirname(os.path.realpath(__file__))


changetimes = read_statistic()

intervals = {
    "second": timedelta(seconds=1),
    "minute": timedelta(minutes=1),
    "day": timedelta(days=1),
    "week": timedelta(days=7),
    "months": timedelta(days=30)
}
start = changetimes["total"][0]
end = changetimes["total"][-1]

# plot totals
for interval_name in ["second", "minute", "day", "week", "months"]:
    interval = intervals[interval_name]
    fig, ax = plt.subplots()
    for project in changetimes:
        plot_total(changetimes[project], project, interval, start, end, ax)
    plt.legend()


    plt.savefig(os.path.join(dir_path, "{}-total.png".format(interval_name)))
    plt.show()
    plt.close('all')

plot_average(changetimes, start)

plot_day_average(changetimes, start)