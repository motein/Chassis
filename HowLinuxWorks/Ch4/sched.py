#!/usr/bin/python3

import sys
import time
import os
from plot import plot

def usage():
    print("""Usage: {} <degree of parallelism>
        * 
After starting load processing that consumes CPU resources for about 100 milliseconds simultaneously on CPU core 0 for the number of <degree of parallelism>, wait for all processes to finish.
        * Export a graph showing the execution results to a file called "<Processing number (0~(Parallelism degree - 1)>.jpg").
        * The x-axis of the graph is the elapsed time [milliseconds] since the start of the process, and the y-axis is the progress [%]""".format(progname, file=sys.stderr))
    sys.exit(1)

# Load applied to preprocessing to find the load suitable for the experiment.
# If this program takes too long to run, reduce the value.
# On the other hand, if the process ends quickly, increase the value.
NLOOP_FOR_ESTIMATION=100000000
nloop_per_msec = None
progname = sys.argv[0]

def estimate_loops_per_msec():
	before = time.perf_counter()
	for _ in  range(NLOOP_FOR_ESTIMATION):
		pass
	after = time.perf_counter()
	return int(NLOOP_FOR_ESTIMATION/(after-before)/1000)

def child_fn(n):
    progress = 100*[None]
    for i in range(100):
        for j in range(nloop_per_msec):
            pass
        progress[i] = time.perf_counter()
    f = open("{}.data".format(n),"w")
    for i in range(100):
        f.write("{}\t{}\n".format((progress[i]-start)*1000,i))
    f.close()
    exit(0)

if len(sys.argv) < 2:
    usage()

concurrency = int(sys.argv[1])

if concurrency < 1:
    print("<Parallelism degree> should be an integer greater than or equal to 1: {}".format(concurrency))
    usage()

# Force execution on CPU core 0
os.sched_setaffinity(0, {0})

nloop_per_msec = estimate_loops_per_msec()

start = time.perf_counter()

for i in range(concurrency):
    pid = os.fork()
    if (pid < 0):
        exit(1)
    elif pid == 0:
        child_fn(i)

for i in range(concurrency):
    os.wait()

plot.plot_sched(concurrency)