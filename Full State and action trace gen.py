

"""
Given a  problem and domain file, runs fast downward to find the the solution, and then ...
To generate traces containing a sequence of ; the propositions of a state first in a list, followed by a grounded action,
and then the resultant state.

Make sure to setup the locations, especially of fastdownward correctly
Install pddlpy to parse the initial state
"""


import subprocess
import os
import pickle
import pddlpy
import copy
from enum import Enum

number_traces = 10
keywords_before_solution = "Actual search time"
keywords_after_solution = "Plan length"
#---for making problem files
logisitics_gen_exec = "./Logistics_pddl/logistics "
#code to generate a random problem space
logistics_config = ["-c 4", "-s 3","-p 1", "-a 1"]
dest_name_suffix = "_".join(logistics_config).replace("-","").replace(" ","")
dest_file_name = "./Logistics_pddl/problem_logistics_"+ dest_name_suffix+".pddl"
#---for FD
fast_downward_exec_loc = "~/FastDownward/fast-downward.py"
fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
domain_file_loc = "./Logistics_pddl/domain.pddl"
problem_file_loc = dest_file_name
solution_file_loc = "./Logistics_pddl/logistics_solution.txt"
pickle_dest_file = str(number_traces)+dest_name_suffix+"_logistics_dataset.p"

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
#==================================================
class Action:
    """
    Contains information about a LIFTED action such as preconditions and effects.
    Has functions that when given a state dict, and parameter instantiation, will give the resultant state dict
    """
    def __init__(self, action_name , parameter_list = [], preconditions_dict = {},pos_effects_dict = {},neg_effects_dict = {}):
        self.action_name = action_name
        self.parameter_list = parameter_list
        self.preconditions_dict = preconditions_dict
        self.pos_effects_dict= pos_effects_dict
        self.neg_effects_dict= neg_effects_dict

    def get_parameter_list(self):
        return self.parameter_list

    def produce_resultant_state_dict(self,parameter_instantiation,starting_state_dict):
        pass
#==================================================
class Action_parser:
    """
    Reads a domain file and produces action objects for each action in it
    """

    class Action_parsing_state(Enum):
        in_limbo = 0
        in_parameters = 1
        in_preconditions = 2
        in_effects = 3
    def __init__(self,domain_file_loc):
        self.action_objects_list = self.parse_domain_file(domain_file_loc)

    def parse_domain_file(self,domain_file_loc):
        """
        :summary: go through the domain and get for each action, parameters, preconditions, effects
        :param domain_file:
        :return: list of action_objects
        """
        ret_action_list = []
        action_start_token  = ":action"
        parameter_start_token  = ":parameter"
        precondition_start_token  = ":precondition"
        effect_start_token  = ":effect"
        parsing_state = self.Action_parsing_state.in_limbo
        #--end class
        action_name = None
        parameter_list = []
        preconditions_dict = {}
        pos_effects_dict = {}
        neg_effects_dict = {}
        with open(domain_file_loc,"r") as domain_file:
            for line in domain_file:
                if action_start_token in line:
                    #create an object with the previous one
                    if action_name != None:
                        #create a new action object
                        ret_action_list.append(\
                            Action(action_name , parameter_list, preconditions_dict ,pos_effects_dict,neg_effects_dict))
                    #--end if
                    #start of a new action
                    parsing_state = self.Action_parsing_state.in_parameters
                    action_name = line.split(action_start_token)[-1].strip()
                elif parameter_start_token in line:
                    parsing_state = self.Action_parsing_state.in_parameters
                elif precondition_start_token in line:
                    parsing_state = self.Action_parsing_state.in_preconditions
                elif effect_start_token in line:
                    parsing_state = self.Action_parsing_state.in_effects
                elif parsing_state == self.Action_parsing_state.in_parameters:
                    line = line.replace("(","").replace(")","").replace("?","").replace("\n","")
                    parameters = line.split(" ")
                    parameter_list += [x for x in parameters if x != '']
                elif parsing_state == self.Action_parsing_state.in_preconditions:
                    line = line.replace("(and","").replace("?","")
                    propositions = line.split(")")
                    for single_proposition in propositions:
                        if "(" in single_proposition:
                            proposition_string = single_proposition.split("(")[-1]
                            proposition_parts_list = proposition_string.split(" ")
                            insert_list_in_dict(proposition_parts_list,preconditions_dict)
                elif parsing_state == self.Action_parsing_state.in_effects:
                    line = line.replace("(and","").replace("?","")
                    propositions = line.split(")")
                    for single_proposition in propositions:
                        if "(" in single_proposition:
                            target_dict = pos_effects_dict
                            if "(not" in single_proposition:
                                target_dict = neg_effects_dict
                                single_proposition = single_proposition.replace("(not","")
                            proposition_string = single_proposition.split("(")[-1]
                            proposition_parts_list = proposition_string.split(" ")
                            insert_list_in_dict(proposition_parts_list,target_dict)
                #end elif parsing_state == self.Action_parsing_state.in_effects:
            #end for loop
        #end with open()
        return ret_action_list
    #---end class method
#---end class





#==============================================================================+++
def convert_dict_to_list(input_dict,prev_key_seq = ""):
    """
    :param state_dict:
    :return:
    """
    ret_list = []
    for single_key in input_dict.keys():
        new_key_seq = prev_key_seq + "_" + single_key
        next_level = input_dict[single_key]
        if type(next_level) == dict:
            sub_list = convert_dict_to_list(next_level,new_key_seq)
            ret_list += sub_list
        elif type(next_level) == list or type(next_level) == tuple: #it ought to be a list or tuple
            for single_entry in next_level:
                ret_list.append(new_key_seq + "_" + single_entry)
        else: # it is a primitive type
            ret_list.append(new_key_seq+"_"+next_level)
        #end if-else
    #end for
    return ret_list





#==============================================================================+++
def convert_to_state_action_list(solution_list):
    """
    :summary : Get the start state from the problem file. Parse each action, and apply it to the start state.
    Get the resultant state and repeat. Each state is converted into a list of propositions and placed in the trace.
    The ground actions are placed in the trace as a list of one
    :param solution_list:
    :return:
    """
    s_a_trace = []
    #get the start state using pddlpy
    pddl_obj = pddlpy.DomainProblem(domain_file_loc, problem_file_loc)
    init_state_prop_set = pddl_obj.initialstate()
    state_dict = {}
    for single_prop in init_state_prop_set:
        curr_prop = single_prop.predicate
        insert_list_in_dict(curr_prop,state_dict)
    #---end for loop making the state dict
    #convert the state dict into a list of propositions
    curr_state = convert_dict_to_list(state_dict)
    s_a_trace.append(curr_state)

    #parse the action, and determine the precondition and effects
    for single_action in solution_list:
        pass


    return s_a_trace



# ==============================================================================+++
action_parser_obj = Action_parser(domain_file_loc)
all_solutions = set()
counter = 0
while len(all_solutions) < number_traces:
    counter +=1
    if counter%100 == 0:
        print("At iteration",counter)
        print("Number solutions",len(all_solutions))
        with open(pickle_dest_file, "wb") as destination:
            pickle.dump(all_solutions, destination)
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
    # print(solution_list)
    if len(solution_list)> 1: #need atleast two actions to have informational value
        solution_list = tuple(solution_list)
        if solution_list not in all_solutions:
            s_a_trace = convert_to_state_action_list(solution_list)
            all_solutions.add(s_a_trace)
#---end outer for



#testing code
# with open(pickle_dest_file, "rb") as source_file:
#     a = pickle.load(source_file)
#     print(a)




