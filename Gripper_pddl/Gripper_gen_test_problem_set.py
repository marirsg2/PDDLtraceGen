
import subprocess
import os
import pickle
import copy
from enum import Enum

number_problems = 14
keywords_before_solution = "Actual search time"
keywords_after_solution = "Plan length"
#---for making problem files
problem_gen_exec = "./gripper "
#code to generate a random problem space
merged_data = []

# all_configs= [["-n 1", "-r 2","-o 5"],["-n 1", "-r 4","-o 5"],["-n 1", "-r 8","-o 5"],["-n 1", "-r 16","-o 5"],["-n 1", "-r 64","-o 5"]]
# all_configs= [["-n 1", "-r 13","-o 10"],["-n 1", "-r 5","-o 10"],["-n 1", "-r 7","-o 7"],["-n 1", "-r 13","-o 5"],
#               ["-n 1", "-r 3","-o 7"],["-n 1", "-r 9","-o 5"],["-n 1", "-r 5","-o 9"]]
#todo I wonder if it learns better when you have a subset of settings varying only one dimension, and another varying only another dimension rather than mixing
all_configs= [["-n 1", "-r 5","-o 5"],["-n 1", "-r 5","-o 10"],["-n 1", "-r 7","-o 7"],["-n 1", "-r 13","-o 5"],
              ["-n 1", "-r 3","-o 7"],["-n 1", "-r 9","-o 5"],["-n 1", "-r 5","-o 9"]]

number_problems = int(number_problems/len(all_configs))
#----------------------
for problem_config in all_configs:
    for problem_idx in range(number_problems):
        print("problem_config = ", problem_config)
        dest_name_suffix = "_".join(problem_config).replace("-","").replace(" ","")+"_"+str(problem_idx+1)
        dest_problem_file_name = "./GripperProblemSet/gripper_problems_" + dest_name_suffix + ".pddl"#this is where the problems problem file generator stores the problem.pddl file
        #---for FD
        fast_downward_exec_loc = "~/Fastdownward/fast-downward.py"
        fd_alias = ""
        # fd_alias = "--alias seq-opt-lmcut"
        fd_alias = "--alias lama-first"
        fd_heuristic_config = ""
        # fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
        domain_file_loc = "./gripper_domain.pddl"
        problem_file_loc = dest_problem_file_name
        solution_file_loc = "./GripperFDSolutionSet/gripper_solution_"+dest_name_suffix+ ".txt"#THIS Is where the solutions from FASTDDOWNWARD are stored, not the traces.

        #---create problem files
        command = problem_gen_exec + " ".join(problem_config)
        os.system(command +" > " + dest_problem_file_name)

        #for gripper the problem generator calls the balls, as objects. need to update problem file
        all_lines = []
        with open(dest_problem_file_name,"r") as src:
            all_lines = [x.replace("- object","- ball") for x in src.readlines()]
        with open(dest_problem_file_name, "w") as dest:
            dest.writelines(all_lines)

        #---NOW we have the problem files ,lets generate the solutions with fast downward
        fd_command = fast_downward_exec_loc + " "+ fd_alias + " " + domain_file_loc + " " + problem_file_loc + " " +fd_heuristic_config
        os.system(fd_command+" > " + solution_file_loc)
    #---end for loop through problem indices
#---end for loop through problems configs



