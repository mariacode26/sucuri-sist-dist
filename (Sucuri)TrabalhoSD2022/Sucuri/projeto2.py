import sys, os, time, math
import re
from pyDF import *
sys.path.append(os.environ['PYDFHOME'])

regex =  '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	
def readFile(args):
	filename = args[0]
	f = open(filename, "r")

	vector = []

	for line in f:
		vector.append(line)

	f.close()

	return nprocs, vector

def filterMails(args):
    sp = args[0]

    aux = sp[1][:-1]
    if re.search(regex,aux):
            return sp[0][:-1]
    else:
            return ""

def printMails(args):
	if args[0] != "":
		print(args[0])


nprocs = int(sys.argv[1])
filename = sys.argv[2]

graph = DFGraph()
sched = Scheduler(graph, nprocs, mpi_enabled = False)

fp = open(filename, "r")

src = Source(fp)
graph.add(src)

nd = FilterTagged(filterMails, 1)
graph.add(nd)

ser = Serializer(printMails, 1)
graph.add(ser)


src.add_edge(nd, 0)
nd.add_edge(ser, 0)


t0 = time.time()
sched.start()
t1 = time.time()

print("Execution time %.3f" %(t1-t0))
