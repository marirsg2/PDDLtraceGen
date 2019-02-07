

"""
This code first generates a barman pddl problem file using a script generator.
It then runs fast downward to find the the solution, and you have to give the problem and domain file
The traces are sequences of list. Each tuple has the propositions of a state first , and the last entry is the action.
For each action there are two entries in the list. A "before/precondition state" with the action, and "After/Effect state" with the same action.
The action is always the last entry

INSTRUCTIONS:
1) Install fastdownward planner
2) Install pddlpy  (used to parse the initial state from the problem file)
3) Make sure to enter the location of fastdownward into the variables in the code correctly.
    "barman_gen_exec"
4) Make sure the barman TYPED_blocks_domain.pddl file is in the "Barman_pddl" folder. This domain file is from the sample
domains you get when you install fast downward. This should already be there, just double-check.

NOTE: In the "Barman_pddl" folder is an executable script called barman that generates the problem.pddl files based
on how many cities, locations and packages you want.

"""

"""
SPECIFIC NOTES to barman

1) in domain file Cannot write "?l ?l1 - level)" 
must write "?l - level ?l1 - level)"

2) In domain file, no tabs, must not have separate lines with only closing brackets or opening brackets. close them all in the last line
and open a bracket with the first line. SEE the example domain file.

3) In domain file, for each action , the parameters MUST be presented in this format. One line per parameter, and starting in separate lines
    :parameters
           (?b - beverage
           ?d - shot
           ?h - hand
           ?s - shaker
           ?l - level
           ?l1 - level)

"""

#Todo Yet to test the plan generation from fast downward. Only got the problem generation done


# CONTINUE DEBUGGING THE DOMAIN PARSER , and check the solution saved


import subprocess
import os
import pickle
import pddlpy
import copy
from enum import Enum

number_traces = 100 #todo note make sure the num goals is high enough to produce the number of traces needed. Also ensure enough shot glasses and cocktails for diverse goals
max_num_goals = 2 #todo note make sure the num goals is high enough to produce the number of traces needed. Also ensure enough shot glasses and cocktails for diverse goals
keywords_before_solution = "Actual search time"
keywords_after_solution = "Plan length"
#---for making problem files
barman_gen_exec = "./Barman_pddl_gen/barman-generator.py "
#code to generate a random problem space
barman_config = ["10", "20","10" , "4562"]# num cocktails, num ingredients, num shots, optional random seed.

dest_name_suffix = "_".join(barman_config).replace("-","").replace(" ","")
dest_problem_file_name = "./Barman_pddl_gen/problem_barman_" + dest_name_suffix + ".pddl"#this is where the barman problem file generator stores the problem.pddl file
#---for FD
fast_downward_exec_loc = "~/FastDownward/fast-downward.py"
fd_heuristic_config = "--heuristic \"hff=ff()\" --heuristic \"hcea=cea()\" --search \"lazy_greedy([hff, hcea], preferred=[hff, hcea])\""
domain_file_loc = "./Barman_pddl_gen/TYPED_barman_domain.pddl"
problem_file_loc = dest_problem_file_name
solution_file_loc = "./Barman_pddl_gen/barman_solution.txt"#THIS Is where the solutions from FASTDDOWNWARD are stored, not the traces.
pickle_dest_file = str(number_traces)+"_"+dest_name_suffix+"_barman_dataset.p" #THE PICKLE file where the generated data (plan traces) are stored

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
def translate_list_by_dict(input_list,translation_dict):
    """
    :param single_precondition:
    :param translation_dict:
    :return:
    """
    ret_list = []
    translation_dict_keys = translation_dict.keys()
    for single_key in input_list:
        if single_key in translation_dict_keys:
            ret_list.append(translation_dict[single_key])
        else:
            ret_list.append(single_key)
        #end if
    #end for
    return ret_list
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
            precondition_parameters = single_precondition.split("_")[1:]
            grounded_precondition_params = "_".join(translate_list_by_dict(precondition_parameters,translation_dict))
            grounded_precondition = precondition_type + "_" + grounded_precondition_params
            if not grounded_precondition in starting_state_set:
                return starting_state_set
        #now convert the positive and negative effects into their grounded form
        for single_neg_effect in self.neg_effects_set:
            #sadly the python str translate functionality does not meet our needs
            eff_type = single_neg_effect.split("_")[0]
            eff_parameters = single_neg_effect.split("_")[1:]
            grounded_eff_params = "_".join(translate_list_by_dict(eff_parameters,translation_dict))
            grounded_eff = eff_type + "_" + grounded_eff_params
            ret_state_set.remove(grounded_eff)
        for single_pos_effect in self.pos_effects_set:
            #sadly the python str translate functionality does not meet our needs
            eff_type = single_pos_effect.split("_")[0]
            eff_parameters = single_pos_effect.split("_")[1:]
            grounded_eff_params = "_".join(translate_list_by_dict(eff_parameters,translation_dict))
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
                    # if action_name.startswith("pour-shot-to-used-shaker"):
                    #     print("catch")
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
                    parameters = [x for x in parameters if x != '']
                    parameter_list.append(parameters[0])
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



def modify_barman_problem_goal(problem_idx, total_num_cocktails, total_num_shots, max_num_goals, dest_problem_file_name):
    """
    :summary: simply change the goal
    :param total_num_cocktails:
    :param num_shorts:
    :param max_num_goals:
    :param dest_problem_file_name:
    :return:
    """

    new_lines = []
    total_num = 0
    cocktail_shot_combo_num =  1
    list_goal_count_index = []
    num_cocktails = total_num_cocktails
    num_shots = total_num_shots

    for i in range(max_num_goals):
        cocktail_shot_combo_num = cocktail_shot_combo_num * num_cocktails * num_shots
        total_num = total_num + cocktail_shot_combo_num
        list_goal_count_index.append(total_num) #this will tell us what number of goals to add in this current problem iter
        num_shots -= 1

    num_goals = 0
    for i in range(len(list_goal_count_index)):
        if problem_idx < list_goal_count_index[i]:
            num_goals = i+1
            break


    with open(dest_problem_file_name,"r") as source_file:
        for idx,curr_line in enumerate(source_file.readlines()):
            if idx == 0: #counter is not 0 based
                if "(define" not in curr_line: #this is because of a strange fast downward line added at the top, and only sometimes
                    continue
            new_lines.append(curr_line)
            if ":goal" in curr_line:
                new_lines.append("(and \n")
                prev_block_size = 1
                allowed_shots = list(range(1,total_num_shots+1))
                for goal_idx in range(num_goals):
                    problem_offset = int(problem_idx / prev_block_size)
                    curr_problem_block = int(problem_offset % list_goal_count_index[goal_idx])
                    allowed_num_shots = total_num_shots - goal_idx # "+1" is not needed since the index is 0-based
                    shot_num = allowed_shots[int(curr_problem_block%allowed_num_shots -goal_idx)] #because the num is 1-based.
                    allowed_shots.remove(shot_num)
                    cocktail_num = int((curr_problem_block/allowed_num_shots) % total_num_cocktails +1)#because the num is 1-based.
                    new_lines.append("(contains shot" +str(shot_num) + " " +"cocktail" + str(cocktail_num)  +" ) \n")
                    prev_block_size = list_goal_count_index[goal_idx]
                #end for
                new_lines.append("))) \n")
                break
            #end if
        #end for
    #end with
    with open(dest_problem_file_name, "w") as dest_file:
        dest_file.writelines(new_lines)
#end function modify barman problem

# action_solutions = set()
counter = 0
command = barman_gen_exec + " ".join(barman_config)
num_cocktails = int(barman_config[0])
num_shots = int(barman_config[2])
#we have already defined num goals
if not(num_cocktails > (num_shots-1)) or not(max_num_goals < num_cocktails):
    raise("ERROR: num cocktails and max_num_goals must be less than shots-1 ")
current_problem_index = 0 #yes we start at 0 zero index
os.system(command +" > " + dest_problem_file_name)
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
    #TODO MODIFY THE BARMAN FILE PROBLEM
    modify_barman_problem_goal(current_problem_index, num_cocktails, num_shots, max_num_goals, dest_problem_file_name)
    current_problem_index += 1

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
    counter = 5
    for single in a:
        print(single)
        counter -= 1
        if counter == 0:
            break


