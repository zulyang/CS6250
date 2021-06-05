from os import listdir
from os.path import isfile, join
from Topology import *
import sys
import filecmp

topo_path = 'test/topos/'  # dir of test topologies
my_log_path = 'test/my_logs/'  # dir for your logs
comp_log_path = 'test/logs/'  # dir for comparing logs
passed = 0
sys.path.insert(0, topo_path)
files = [f for f in listdir(topo_path) if isfile(join(topo_path, f))]
total = len(files)
for file in files:
    topo_name = file[:-3]
    # Populate the topology
    topo = Topology(topo_name)
    # Run the topology.
    topo.run_spanning_tree()
    # Close the logfile
    topo.log_spanning_tree(my_log_path + topo_name + '.log')
    # compare 
    # Thanks to Tsun Ku for fixing cross OS suppoort !!!
    # with open(my_log_path + topo_name + '.log') as mine, open(comp_log_path + topo_name + '.log') as others:
    #     equal = mine.readlines() == others.readlines()
    #     if not equal:
    #         print(topo_name,  '=', equal)
 
    with open(my_log_path + topo_name + '.log') as mine, open(comp_log_path + topo_name + '.log') as others:
        if(mine.readlines() == others.readlines()):
            passed += 1
        else:
            print(topo_name,  '=', 'False')
    print(f"{passed}/{total} Tests Passed!")