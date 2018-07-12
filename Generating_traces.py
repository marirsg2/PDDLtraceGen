

"""
:summary: This script generates the traces for doc2vec
Each trace is tagged with the context, which maybe the pertinent initial and goal propositions, or other ctx info.
"""

import subprocess
import os
import pickle

number_traces = 10
pickle_dest_file = "logistics_dataset.p"
keywords_before_solution = "Actual search time"
keywords_after_solution = "Plan length"
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


all_solutions = []
for i in range(number_traces):
    #---create problem files
    command = logisitics_gen_exec + " ".join(logistics_config)
    os.system(command+" > " + dest_file_name)
    #---NOW we have the problem files ,lets generate the solutions with fast downward
    fd_command = fast_downward_exec_loc + " " + domain_file_loc + " " + problem_file_loc + " " +fd_heuristic_config
    os.system(fd_command+" > " + solution_file_loc)
    #---now extract the solution
    solution_list = []
    with open(solution_file_loc,"r") as solution_file:
        all_lines = solution_file.readlines()
        start_of_solution = False
        for single_line in all_lines:
            if keywords_before_solution in single_line:
                start_of_solution = True
                continue# the NEXT line will have the start of the solution
            if keywords_after_solution in single_line:
                break #end of the solution
            if start_of_solution:
                the_word = single_line.split("(")[0].replace(" ","_")[:-1]# we get rid of trailing info like "(1)\n"
                solution_list.append(the_word)
        #---end for
    #---end with
    print(solution_list)
    all_solutions.append(solution_list)
#---end outer for
with open(pickle_dest_file, "wb") as destination:
    pickle.dump(all_solutions,destination)


with open(pickle_dest_file, "rb") as source_file:
    a = pickle.load(source_file)
    print(a)




