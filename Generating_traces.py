

"""
:summary: This script generates the traces for doc2vec
Each trace is tagged with the context, which maybe the pertinent initial and goal propositions, or other ctx info.
"""

import subprocess
import os

number_traces  = 10
#---for making problem files
logisitics_gen_exec = "./Logistics_pddl/logistics "
#code to generate a random problem space
logistics_config = ["-c 4", "-s 3","-p 1", "-a 2"]
dest_name_suffix = "_".join(logistics_config).replace("-","").replace(" ","")
dest_file_name = "./Logistics_pddl/problem_logistics_"+ dest_name_suffix+".pddl"
#---for FD
fast_downward_exec_loc = "~/FastDownward/fast-downward.py"
fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
domain_file_loc = "./Logistics_pddl/domain.pddl"
problem_file_loc = dest_file_name
solution_file_loc = "./Logistics_pddl/logistics_solution.txt"

#---create problem files
command = logisitics_gen_exec + " ".join(logistics_config)
os.system(command+" > " + dest_file_name)
#---NOW we have the problem files ,lets generate the solutions with fast downward
fd_command = fast_downward_exec_loc + " " + domain_file_loc + " " + problem_file_loc + " " +fd_heuristic_config
os.system(fd_command+" > " + solution_file_loc)
