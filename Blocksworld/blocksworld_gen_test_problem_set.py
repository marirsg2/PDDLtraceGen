
import subprocess
import os
import shutil
import pickle
import copy
from enum import Enum
import random

problems_per_setting = 5#this is problems per setting
keywords_before_solution = "Actual search time"
keywords_after_solution = "Plan length"
#---for making problem files

#code to generate a random problem space
merged_data = []

problems_folder = "BlocksworldProblemSet"
solutions_folder = "BlocksworldFDSolutionSet"


all_configs= [[5,4],[5,5], [10,6],[10,8],[12,5],[12,12]]
random.seed(1)



#================================================
def get_all_stacked(block_a,stacking_dict):
    stacked_list = [block_a]
    while True:
        try:
            stacked_list.append(stacking_dict[stacked_list[-1]])
        except KeyError:
            return stacked_list
#================================================
def generate_blocksworld_problem(num_blocks, dest_file_name, num_blocks_in_goal = None):
    """

    :param num_blocks:
    :param num_blocks_in_goal:
    :return:
    """
    if num_blocks_in_goal == None:
        num_blocks_in_goal = num_blocks
    block_obj_list = ["b"+str(x) for x in range(num_blocks)]
    goal_blocks_list = random.sample(block_obj_list,num_blocks_in_goal)
    clear_blocks = copy.deepcopy(block_obj_list)
    stacking_dict = {}

    with open(dest_file_name,"w") as dest_file:
        dest_file.write("(define (problem BW-rand-" + str(num_blocks)+")\n")
        dest_file.write("(:domain blocksworld)\n")
        dest_file.write("(:objects " + " ".join(block_obj_list) + " - block)\n")
        dest_file.write("(:init \n")
        dest_file.write("")
        dest_file.write("(handempty)\n")
        for block in block_obj_list:
            #either choose a clear block to stack on, or be on table
            avail_blocks = copy.deepcopy(clear_blocks)
            avail_blocks = [x for x in avail_blocks if x not in get_all_stacked(block,stacking_dict)]
            available_choices = avail_blocks + ["ontable"]
            pos = random.choice(available_choices)
            if pos == 'ontable':
                dest_file.write("(ontable "+block+")\n")
            else:#it will be placed on a block
                dest_file.write("(on "+block +' '+pos+")\n")
                stacking_dict[pos] = block
                clear_blocks.remove(pos)
        #end for loop
        for clear_block in clear_blocks: #those left clear
            dest_file.write("(clear " + clear_block+")\n")
        dest_file.write(")\n")
        #===now write the goals
        dest_file.write("(:goal\n")
        dest_file.write("(and\n")
        clear_blocks = copy.deepcopy(goal_blocks_list)
        stacking_dict = {}
        for block in goal_blocks_list:
            #either choose a clear block to stack on, or be on table
            avail_blocks = copy.deepcopy(clear_blocks)
            avail_blocks = [x for x in avail_blocks if x not in get_all_stacked(block,stacking_dict)]
            available_choices = avail_blocks + ["ontable"]
            pos = random.choice(available_choices)
            if pos == 'ontable':
                dest_file.write("(ontable "+block+")\n")
            else:#it will be placed on a block
                dest_file.write("(on "+block +' '+pos+")\n")
                stacking_dict[pos] = block
                clear_blocks.remove(pos)
        #end for loop through goal blocks
        dest_file.write(")\n)\n)")
    #end with statement
#=========================================================

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
    for problem_idx in range(problems_per_setting):
        print("problem_config = ", problem_config)
        string_config = [str(x) for x in problem_config]
        dest_name_suffix = "_".join(string_config).replace("-","").replace(" ","")+"_"+str(problem_idx+1)
        dest_problem_file_name = "./" +problems_folder +"/blocksworld_problems_" + dest_name_suffix + ".pddl"#this is where the problems problem file generator stores the problem.pddl file
        #---for FD
        fast_downward_exec_loc = "~/Fastdownward/fast-downward.py"
        fd_alias = ""
        fd_alias = "--alias lama-first"
        fd_heuristic_config = ""
        # fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
        domain_file_loc = "./blocksworld_domain.pddl"
        problem_file_loc = dest_problem_file_name
        solution_file_loc = "./"+solutions_folder +  "/blocksworld_solution_"+dest_name_suffix+ ".txt"#THIS Is where the solutions from FASTDDOWNWARD are stored, not the traces.

        #---create problem files
        generate_blocksworld_problem(problem_config[0], problem_file_loc, problem_config[1])


        #---NOW we have the problem files ,lets generate the solutions with fast downward
        fd_command = fast_downward_exec_loc + " "+ fd_alias + " " + domain_file_loc + " " + problem_file_loc + " " +fd_heuristic_config
        os.system(fd_command+" > " + solution_file_loc)
    #---end for loop through problem indices
#---end for loop through problems configs



