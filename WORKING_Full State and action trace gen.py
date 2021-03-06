

"""
This code first generates a logistics pddl problem file using a script generator.
It then runs fast downward to find the the solution, and you have to give the problem and domain file
The traces are sequences of list. Each tuple has the propositions of a state first , and the last entry is the action.
For each action there are two entries in the list. A "before/precondition state" with the action, and "After/Effect state" with the same action.
The action is always the last entry

INSTRUCTIONS:
1) Install fastdownward planner
2) Install pddlpy  (used to parse the initial state from the problem file)
3) Make sure to enter the location of fastdownward into the variables in the code correctly.
    "logisitics_gen_exec"
4) Make sure the logistics TYPED_blocks_domain.pddl file is in the "Logistics_pddl" folder. This domain file is from the sample
domains you get when you install fast downward. This should already be there, just double-check.

NOTE: In the "Logistics_pddl" folder is an executable script called logistics that generates the problem.pddl files based
on how many cities, locations and packages you want.

"""


#FOR 4 CITIES, 3 LOC, 1 AIRPLANE. tHERE ARE 3888 POSSIBLE initial starting cases. with 12 possible goal locations that
#makes 46k traces. Factor in ordering actions, and you have ~120k traces.


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
logistics_config = ["-c 8", "-s 4","-p 1", "-a 4"]# ["-c 4", "-s 3","-p 1", "-a 1"] means 4 cities, 3 locations in each city, 1 package, and 1 airplane
dest_name_suffix = "_".join(logistics_config).replace("-","").replace(" ","")
dest_problem_file_name = "./Logistics_pddl/problem_logistics_" + dest_name_suffix + ".pddl"#this is where the logistics problem file generator stores the problem.pddl file
#---for FD
fast_downward_exec_loc = "~/FastDownward/fast-downward.py"
fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
domain_file_loc = "./Logistics_pddl/logistics_domain.pddl"
problem_file_loc = dest_problem_file_name
solution_file_loc = "./Logistics_pddl/logistics_solution.txt"#THIS Is where the solutions from FASTDDOWNWARD are stored, not the traces.
pickle_dest_file = str(number_traces)+dest_name_suffix+"_logistics_dataset.p" #THE PICKLE file where the generated data (plan traces) are stored

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
    for single_key in translation_dict:
        if single_key in input_string:
            input_string = input_string.replace(single_key,translation_dict[single_key])
        #end if
    #end for
    return input_string
#==================================================
class Action:
    """
    Contains information about a LIFTED action such as preconditions and effects.
    Has functions that when given a state dict, and parameter instantiation, will give the resultant state dict
    """
    def __init__(self, action_name , parameter_list = [], preconditions_dict = {},pos_effects_dict = {},neg_effects_dict = {}):
        self.action_name = str.lower(action_name)
        self.parameter_list = parameter_list
        self.preconditions_set = set(convert_dict_to_list(preconditions_dict))
        self.pos_effects_set = set(convert_dict_to_list(pos_effects_dict))
        self.neg_effects_set = set(convert_dict_to_list(neg_effects_dict))

    def get_parameter_list(self):
        return self.parameter_list

    def produce_resultant_state_dict(self,action_name,starting_state_set):
        """
        :param parameter_instantiation:
        :param starting_state_dict:
        :return:
        """
        ret_state_set = starting_state_set
        #parse the action name to get the parameter instantiation
        action_parts = action_name.split("_")
        action_name = str.lower(action_parts[0])
        param_instantiation = action_parts[1:]
        # build a map from parameter name to the instantiation, assume the lists are in the same order
        translation_dict = dict(zip(self.parameter_list,param_instantiation))
        #translate and check if the preconditions hold
        for single_precondition in self.preconditions_set:
            #sadly the python str translate functionality does not meet our needs
            precondition_type = single_precondition.split("_")[0]
            precondition_parameters = "_".join(single_precondition.split("_")[1:])
            grounded_precondition_params = translate_by_dict(precondition_parameters,translation_dict)
            grounded_precondition = precondition_type + "_" + grounded_precondition_params
            if not grounded_precondition in starting_state_set:
                return starting_state_set
        #now convert the positive and negative effects into their grounded form
        for single_neg_effect in self.neg_effects_set:
            #sadly the python str translate functionality does not meet our needs
            eff_type = single_neg_effect.split("_")[0]
            eff_parameters = "_".join(single_neg_effect.split("_")[1:])
            grounded_eff_params = translate_by_dict(eff_parameters,translation_dict)
            grounded_eff = eff_type + "_" + grounded_eff_params
            ret_state_set.remove(grounded_eff)
        for single_pos_effect in self.pos_effects_set:
            #sadly the python str translate functionality does not meet our needs
            eff_type = single_pos_effect.split("_")[0]
            eff_parameters = "_".join(single_pos_effect.split("_")[1:])
            grounded_eff_params = translate_by_dict(eff_parameters,translation_dict)
            grounded_eff = eff_type + "_" + grounded_eff_params
            ret_state_set.add(grounded_eff)


        return ret_state_set

#==================================================
class Domain_manipulator:
    """
    Reads a domain file and produces action objects for each action in it
    """

    class Action_parsing_state(Enum):
        not_started = 0
        in_parameters = 1
        in_preconditions = 2
        in_effects = 3
    def __init__(self,domain_file_loc):
        self.action_dict = self.parse_domain_file(domain_file_loc)

    def parse_domain_file(self,domain_file_loc):
        """
        :summary: go through the domain and get for each action, parameters, preconditions, effects
        :param domain_file:
        :return: list of action_objects
        """
        ret_action_dict = {}
        action_start_token  = ":action"
        parameter_start_token  = ":parameter"
        precondition_start_token  = ":precondition"
        effect_start_token  = ":effect"
        parsing_state = self.Action_parsing_state.not_started
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
                        ret_action_dict[action_name] =\
                            Action(action_name , parameter_list, preconditions_dict ,pos_effects_dict,neg_effects_dict)
                    #--end if
                    #start of a new action
                    action_name = line.split(action_start_token)[-1].strip()
                    action_name = str.lower(action_name)
                    parameter_list = []
                    preconditions_dict = {}
                    pos_effects_dict = {}
                    neg_effects_dict = {}
                    parsing_state = self.Action_parsing_state.in_parameters
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
            if action_name != None:
                # create a new action object
                ret_action_dict[action_name] = \
                    Action(action_name, parameter_list, preconditions_dict, pos_effects_dict, neg_effects_dict)
        #end with open()
        return ret_action_dict
    #---end class method
    # =============================================================================+++
    # =============================================================================+++
    def apply_action(self,state_proposition_set, action_string):
        """
        :summary: The action name will be parsed, state propositions are strings.
        :param state_proposition_set:
        :param action_name:
        :return:
        """
        #simply apply the action with the right name
        action_name = action_string.split("_")[0]
        return self.action_dict[action_name].produce_resultant_state_dict(action_string, state_proposition_set)
#---end class

#=============================================================================+++
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
        curr_prop = [str.lower(x) for x in curr_prop]
        insert_list_in_dict(curr_prop,state_dict)
    #---end for loop making the state dict
    #convert the state dict into a list of propositions
    curr_state = convert_dict_to_list(state_dict)
    prev_state = curr_state
    for single_action in solution_list:
        curr_state = domain_parser_obj.apply_action(set(curr_state),single_action)
        s_a_trace.append(tuple(list(prev_state) + ["ACTION_"+single_action]))#the order of propositions does not matter. They all connect to each other
        s_a_trace.append(tuple(list(curr_state) + ["ACTION_"+single_action]))#the order of propositions does not matter. They all connect to each other
        prev_state = curr_state
    #---end for loop

    return s_a_trace



# ==============================================================================+++
domain_parser_obj = Domain_manipulator(domain_file_loc)
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
    command = logisitics_gen_exec + " ".join(logistics_config)
    os.system(command +" > " + dest_problem_file_name)
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
        s_a_trace = convert_to_state_action_list(solution_list)
        s_a_trace = tuple(s_a_trace)
        all_solutions.add(s_a_trace)
#---end outer for

with open(pickle_dest_file, "wb") as destination:
    pickle.dump(all_solutions, destination)

# testing code
with open(pickle_dest_file, "rb") as source_file:
    a = pickle.load(source_file)
    for single in a:
        print(single)


