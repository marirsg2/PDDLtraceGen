

"""
Gripper domain
sources: http://www.plg.inf.uc3m.es/ipc2011-learning/Domains.html

The domain file looks properly typed, but the problem file treats all as objects

May need to process the problem file to type the objects in the ":objects" section

"""


#FOR 4 CITIES, 3 LOC, 1 AIRPLANE. tHERE ARE 3888 POSSIBLE initial starting cases. with 12 possible goal locations that
#makes 46k traces. Factor in ordering actions, and you have ~120k traces.


import subprocess
import os
from shutil import copyfile
import pickle
import pddlpy
import copy
import random
from enum import Enum

number_traces = 2000
keywords_before_solution = "Actual search time"
keywords_after_solution = "Plan length"
#---for making problem files
#code to generate a random problem space
merged_data = []
storage_folder = "/home/yochan-ubuntu19/workspace/PDDLtraceGen/Blocksworld"
domain_name = "blocksworld" #for the lisp directory
pickle_dest_file = "./Blocksworld/JPMC_GenPlan_Blocksworld.p"  # THE PICKLE file where the generated data (plan traces) are stored
home_dir = "~"
#todo ALSO UPDATE THE FASTDOWNWARD locations for domain and problem done in the for loop through configs
lisp_plan_to_state_seq_base_folder ="/home/yochan-ubuntu19/workspace/deepplan/dist"
# lisp_plan_to_state_seq_base_folder = home_dir + "/workspace/deepplan/dist"
"""
configs are 
num blocks, num blocks in goal.
latter must be greater than former

"""
all_configs= [[3,3],[5,5],[5,3], [10,3],[10,5],[10,10]]
number_traces = int(number_traces/len(all_configs))


#================================================
def check_if_stacked(block_a, block_b, stacking_dict):
    ret_val = False
    lower_block = block_a
    try:
        upper_block = stacking_dict[lower_block]
        if upper_block == block_b:
            return True
        else:
            lower_block = upper_block

    except KeyError:
        pass
    return ret_val

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
            avail_blocks = [x for x in clear_blocks if x not in get_all_stacked(block,stacking_dict)]
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
        #now write the goals
        dest_file.write("(:goal\n")
        dest_file.write("(and\n")
        clear_blocks = copy.deepcopy(goal_blocks_list)
        for block in goal_blocks_list:
            #either choose a clear block to stack on, or be on table
            avail_blocks = copy.deepcopy(clear_blocks)
            avail_blocks = [x for x in clear_blocks if x not in get_all_stacked(block,stacking_dict)]
            available_choices = avail_blocks + ["ontable"]
            pos = random.choice(available_choices)
            if pos == 'ontable':
                dest_file.write("(ontable "+block+")\n")
            else:#it will be placed on a block
                dest_file.write("(on "+block +' '+pos+")\n")
                clear_blocks.remove(pos)
        #end for loop through goal blocks
        dest_file.write(")\n)\n)")
    #end with statement
#=========================================================    

# NEXT the action class for "pick" has no parameters, understand and fix this



#----------------------
for problem_config in all_configs:
    print("problem_config = ", problem_config)
    string_config = [str(x) for x in problem_config]
    dest_name_suffix = "_".join(string_config).replace("-","").replace(" ","")
    dest_problem_file_name = "./Blocksworld/blocksworld_problems_" + dest_name_suffix + ".pddl"#this is where the problems problem file generator stores the problem.pddl file
    #---for FD
    fast_downward_exec_loc = "~/Fastdownward/fast-downward.py"
    # fd_alias = ""
    fd_alias = "--alias seq-opt-lmcut"
    fd_heuristic_config = ""
    # fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
    domain_file_loc = "./Blocksworld/blocksworld_domain.pddl"
    problem_file_loc = dest_problem_file_name
    solution_file_loc = "./Blocksworld/blocksworld_solution.txt"#THIS Is where the solutions from FASTDDOWNWARD are stored, not the traces.

    #==============================================================================+++
    def insert_list_in_dict(input_list,dest_dict):
        """

        :param dest_dict:
        :param input_list:
        :return:
        """

        curr_prop = input_list
        current_dict = dest_dict
        while len(curr_prop) > 2:
            if not curr_prop[0] in current_dict.keys():
                current_dict[curr_prop[0]] = {}
            #end if
            current_dict = current_dict[curr_prop[0]]
            curr_prop = curr_prop[1:]
        #---end while
        try:
            current_dict[curr_prop[0]].append(curr_prop[1])
        except:
            current_dict[curr_prop[0]] = [curr_prop[1]]



    #==============================================================================+++
    def convert_dict_to_list(input_dict,prev_key_seq = ""):
        """
        :param state_dict:
        :return:
        """
        ret_list = []
        for single_key in input_dict.keys():
            new_key_seq = prev_key_seq + "_" + single_key
            if prev_key_seq == "":
                new_key_seq = single_key
            next_level = input_dict[single_key]
            if type(next_level) == dict:
                sub_list = convert_dict_to_list(next_level,new_key_seq)
                ret_list += sub_list
            elif type(next_level) == list or type(next_level) == tuple: #it ought to be a list or tuple
                for single_entry in next_level:
                    ret_list.append(str.lower(new_key_seq + "_" + single_entry))
            else: # it is a primitive type
                ret_list.append(str.lower(new_key_seq+"_"+next_level))
            #end if-else
        #end for
        return ret_list
    #==================================================
    def translate_by_dict(input_string,translation_dict):
        """
        :param single_precondition:
        :param translation_dict:
        :return:
        """
        input_string_parts = input_string.split("_")
        translated_parts = []
        for single_part in input_string_parts:
            if single_part in translation_dict.keys():
                translated_parts.append(translation_dict[single_part])
            else:
                translated_parts.append(single_part)
        input_string = "_".join(translated_parts)
        # for single_key in translation_dict:
        #     if single_key in input_string:
        #         input_string = input_string.replace(single_key,translation_dict[single_key])
        #     #end if
        # #end for
        return input_string
    


    #=============================================================================+++
    def get_goals():
        pddl_obj = pddlpy.DomainProblem(domain_file_loc, problem_file_loc)
        return tuple(["_".join(x.predicate) for x in pddl_obj.goals()])
    #=============================================================================+++

    all_solutions = set()

    # with open(pickle_dest_file, "rb") as source_file:
    #     all_solutions = pickle.load(source_file)


    # action_solutions = set()
    counter = 0
    while len(all_solutions) < number_traces:
        counter +=1
        if counter%10 == 0:
            print("At iteration", counter)
            print("Number solutions", len(all_solutions))
        if counter%1000 == 0:
            print("At iteration",counter)
            print("Number solutions",len(all_solutions))
            with open(pickle_dest_file, "wb") as destination:
                pickle.dump(all_solutions, destination)
        #---create problem files
        generate_blocksworld_problem(problem_config[0],dest_problem_file_name,problem_config[1])

        #---NOW we have the problem files ,lets generate the solutions with fast downward
        fd_command = fast_downward_exec_loc + " "+ fd_alias + " " + domain_file_loc + " " + problem_file_loc + " " +fd_heuristic_config
        os.system(fd_command + " > " + solution_file_loc)
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
                    the_word = "("+single_line.split("(")[0][:-1]+")"# we get rid of trailing info like "(1)\n"
                    solution_list.append(the_word)
            #---end for
        #---end with
        # print(solution_list)
        if len(solution_list) == 0:
            continue
        solution_action_seq_string = '\"('+ " ".join(solution_list) + ')\"'
        os.system("cp " + problem_file_loc + " " + lisp_plan_to_state_seq_base_folder + "/planning/sayphi/domains/blocksworld/probsets/test.pddl")

        cwd= os.getcwd()
        #use daniels lisp code to convert the action sequence into a state sequence
        os.chdir(lisp_plan_to_state_seq_base_folder)
        command_to_exec ="./get-state.sh " + solution_action_seq_string + " " +domain_name + " domain.pddl test.pddl "\
                  +storage_folder+"/state-list.txt"
        os.system(command_to_exec)
        os.chdir(cwd)
        #get the solution from the state list file
        with open(storage_folder+"/state-list.txt","r") as src:
            all_solution_lines = src.readlines()
        #each line of the solution is a full state, ('at_ball6_room10', 'at_ball1_room7',...)
        single_seq = []
        for single_line in all_solution_lines:
            single_state = []
            state_line = single_line.lower().replace("\n","")
            for proposition in state_line.split(","):
                single_state.append(proposition.strip().replace(" ","_") )
            single_seq.append(tuple(single_state))
        #---end for loop through solution
        single_seq = tuple(single_seq)
        if len(solution_list) > 1:  # need atleast two actions to have informational value
            goals = get_goals()
            for seq_idx in range(len(single_seq)):
                all_solutions.add((single_seq[seq_idx], goals, len(single_seq) - (seq_idx + 1)) )
            # end for loop
    #---end outer for
    merged_data += all_solutions
#---end for loop through problems configs

# with open(pickle_dest_file, "wb") as destination:
#     pickle.dump(merged_data, destination)
with open(pickle_dest_file, "wb") as destination:
    pickle.dump(merged_data, destination)

# testing code
with open(pickle_dest_file, "rb") as source_file:
    a = pickle.load(source_file)
    for single in a:
        print(single)


