
import subprocess
import os
import shutil
import pickle
import copy
from enum import Enum

number_problems = 30
keywords_before_solution = "Actual search time"
keywords_after_solution = "Plan length"
#---for making problem files
problem_gen_exec = "./gripper "
#code to generate a random problem space
merged_data = []

problems_folder = "GripperProblemSet"
solutions_folder = "GripperFDSolutionSet"


all_configs= [["-n 1", "-r 2","-o 100"],["-n 1", "-r 5","-o 13"],["-n 1", "-r 9","-o 7"],["-n 1", "-r 11","-o 6"],
              ["-n 1", "-r 4","-o 8"],["-n 1", "-r 15","-o 15"]]





number_problems = int(number_problems/len(all_configs))

#---clear the folders
# for folder in [problems_folder,solutions_folder]:
for folder in [solutions_folder]:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

#----------------------
for problem_config in all_configs:
    for problem_idx in range(number_problems):
        print("problem_config = ", problem_config)
        dest_name_suffix = "_".join(problem_config).replace("-","").replace(" ","")+"_"+str(problem_idx+1)
        dest_problem_file_name = "./" +problems_folder +"/gripper_problems_" + dest_name_suffix + ".pddl"#this is where the problems problem file generator stores the problem.pddl file
        #---for FD
        fast_downward_exec_loc = "~/Fastdownward/fast-downward.py"
        fd_alias = ""
        fd_alias = "--alias lama-first"
        fd_heuristic_config = ""
        # fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
        domain_file_loc = "./gripper_domain.pddl"
        problem_file_loc = dest_problem_file_name
        solution_file_loc = "./"+solutions_folder +  "/gripper_solution_"+dest_name_suffix+ ".txt"#THIS Is where the solutions from FASTDDOWNWARD are stored, not the traces.

        #---create problem files
        # !!!!!!!!!!!!!!!!
        # IMPORTANT note if you COMMENT out the following 2 lines, then it will reuse the problem file already there,
        #  this allows you to make modifications to them. and see the assoc solutions
        # make sure to NOT empty the problem folder, and only empty the solution folder
        # command = problem_gen_exec + " ".join(problem_config)
        # os.system(command +" > " + dest_problem_file_name)

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



