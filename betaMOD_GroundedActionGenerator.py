

"""


Very sensitive to the position of brackets, this code is not yet robust. In the action definition for each of the sections
the bracket cannot be in a line by itself.

1)Takes a problem and domain file and generates all the possible grounded actions.
2)It assumes only the static fluents need to be satisfied in the fluents, and that the other fluents can be satisfied
through some walk through the domain graph.

IN THE PDDL FILES FOR EVERY SECTION HEADER, LIKE types: or predicates:
please start the actual content in the next line

Process:

Parse the problem file and build
1) Dict of object type to objects
2) All proposition types and Dict of the start state of the world

Parse Domain file and build
1) Action model as a dict with key as the name, fluents, positive effects, negative effects
2) as you build the action model, NOTE the propositions that CHANGE. These are the NON-STATIC fluents
3) We then take the difference of all fluent types with the non-static fluents as the set of static fluents.
These are the only fluents we check for in the state of the world. All others are just grounded and assumed to be possible

"""




import subprocess
import os
import pickle
import pddlpy
import copy
from enum import Enum

domain_file_loc = "./Logistics_pddl/TYPED_MODlogisticsDomain.pddl"
problem_file_loc = "./Logistics_pddl/TYPED_problem_MODlogistics_c8_s4_p1_a4.pddl"
pickle_dest_file =  "logistics_actionsGrounding_c8_s4_p1_a4.p" #THE PICKLE file where the generated data (plan traces) are stored

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
    def __init__(self, action_name , parameter_name_type_dict = {}, preconditions_dict = {},pos_effects_dict = {},neg_effects_dict = {}):
        self.action_name = str.lower(action_name)
        self.parameter_name_type_dict = parameter_name_type_dict
        self.preconditions_set = set(convert_dict_to_list(preconditions_dict))
        self.pos_effects_set = set(convert_dict_to_list(pos_effects_dict))
        self.neg_effects_set = set(convert_dict_to_list(neg_effects_dict))
        self.static_preconditions_set = set()

    def get_parameter_list(self):
        return self.parameter_name_type_dict

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
        parameter_variables = list(self.parameter_name_type_dict.keys())
        translation_dict = dict(zip(parameter_variables, param_instantiation))
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

    def set_static_preconditions(self,static_preconditions_set):
        """
        :summary: see name
        :param static_fluents_set:
        :return:
        """
        self.static_preconditions_set = static_preconditions_set

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
        in_types = 4 #speaking not an action parsing state but part of processing the domain file
    def __init__(self,domain_file_loc):

        self.to_lower_type_dict = {}
        self.to_upper_type_dict = {}
        self.non_static_fluents_set = set()
        self.actionObj_dict = self.parse_domain_file(domain_file_loc)
        self.process_for_static_fluents()

    def parse_domain_file(self,domain_file_loc):
        """
        :summary: go through the domain and get for each action, parameters, preconditions, effects
        :param domain_file:
        :return: list of action_objects
        """
        ret_action_dict = {}

        types_start_token  = ":types"
        action_start_token  = ":action"
        parameter_start_token  = ":parameter"
        precondition_start_token  = ":precondition"
        effect_start_token  = ":effect"
        parsing_state = self.Action_parsing_state.not_started
        #--end class
        action_name = None
        parameter_name_type_dict = {}
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
                            Action(action_name , parameter_name_type_dict, preconditions_dict ,pos_effects_dict,neg_effects_dict)
                    #--end if
                    #start of a new action
                    action_name = line.split(action_start_token)[-1].strip()
                    action_name = str.lower(action_name)
                    parameter_name_type_dict = {}
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
                elif types_start_token in line:
                    parsing_state = self.Action_parsing_state.in_types

                elif parsing_state == self.Action_parsing_state.in_types:
                    line_parts = line.split("-")
                    if len(line_parts) < 2:#not a valid line
                        continue
                    object_mapping_values = line_parts[0].split(" ")
                    object_mapping_values = [x.lower() for x in object_mapping_values if x != '']
                    object_mapping_key = line_parts[1].strip().lower()
                    object_mapping_key = object_mapping_key.replace(")","")
                    self.to_lower_type_dict[object_mapping_key] = object_mapping_values
                    for single_lower_type in object_mapping_values:
                        try:
                            self.to_upper_type_dict[single_lower_type].append(object_mapping_key)
                        except KeyError:
                            self.to_upper_type_dict[single_lower_type] = [object_mapping_key]
                    #end for
                    if ")" in line:# then it is the end of this section
                        parsing_state = self.Action_parsing_state.not_started

                elif parsing_state == self.Action_parsing_state.in_parameters:
                    line = line.replace("(","").replace(")","").replace("?","").replace("\n","")
                    parameter_parts = (line.replace(" ","")).split("-")
                    parameter_name_type_dict[parameter_parts[0].lower()] = parameter_parts[1].lower()
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
                    Action(action_name, parameter_name_type_dict, preconditions_dict, pos_effects_dict, neg_effects_dict)
        #end with open()
        return ret_action_dict
    #---end class method
    # =============================================================================+++
    # =============================================================================+++
    def process_for_static_fluents(self):
        """
        :summary: go through the action dict and for each effect (pos and negative) save the fluents that were changed
        :return:
        """
        #first find all the NON-static fluents, then update the action object to store the static preconditions in it
        for single_action in self.actionObj_dict.keys():
            all_changes_fluents = self.actionObj_dict[single_action].pos_effects_set.union(self.actionObj_dict[single_action].neg_effects_set)
            for single_eff in all_changes_fluents:
                eff_parts = single_eff.split("_")
                eff_subj_type = self.actionObj_dict[single_action].parameter_name_type_dict[eff_parts[1]]
                self.non_static_fluents_set.add((eff_parts[0] + "_" + eff_subj_type).lower())#format <property_name> <object assoc to property>  eg: in_city_tLocation
                #todo UNSURE ABOUT THE FOLLOWING, it is NECESSARY in some cases. Eg: in_tAirplane_tloc may appear static, because only in_tAirplaneAccess0_tloc changes .
                #also add all derived object types, even if it does not exist as a valid fluent
                for single_upper_type in self.to_upper_type_dict[eff_subj_type]:
                    if single_upper_type == "object":
                        continue# we only ignore the default object type
                    self.non_static_fluents_set.add((eff_parts[0] + "_" + single_upper_type).lower())


        #now actually update the action model to store the static preconditions
        for single_action in self.actionObj_dict.keys():
            static_preconditions = set()
            curr_action = self.actionObj_dict[single_action]
            for single_precondition in curr_action.preconditions_set:
                if "not" in single_precondition:
                    single_precondition = single_precondition.replace("not","").replace("(","").replace(")","")
                precondition_parts = single_precondition.split("_")
                lifted_precondition_parts = [precondition_parts[0]] + [curr_action.parameter_name_type_dict[x]  for x in precondition_parts[1:]]
                lifted_precondition_type = "_".join(lifted_precondition_parts[:-1]) # we are only look at things as STATE VARIABLES . If they are static or not
                if lifted_precondition_type not in self.non_static_fluents_set:
                    static_preconditions.add(single_precondition)
            #end for loop
            curr_action.set_static_preconditions(static_preconditions)
        #end outer for loop


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
        return self.actionObj_dict[action_name].produce_resultant_state_dict(action_string, state_proposition_set)

    # =========================================================
    # =========================================================
    def get_all_parameter_groundings(self,action_name,problem_parser_obj):
        """
        :summary: find all possible groundings that pass the static preconditions.
        :param problem_parser_obj:
        :return:
        """
        valid_groundings = set()
        actionObj = self.actionObj_dict[action_name]
        parameter_dict = actionObj.parameter_name_type_dict
        parameter_keys = sorted(list(parameter_dict.keys()))
        #get the parameter object types to search in the problem file
        parameter_types = []
        for single_parameter in parameter_keys:
            parameter_types.append(parameter_dict[single_parameter].lower())
        parameter_possible_values = []
        for single_type in parameter_types:
            parameter_possible_values.append(problem_parser_obj.obj_dict[single_type])
        idx_list = [0]*len(parameter_possible_values)
        #the following is a very involved command and condition.
        #it checks if each of the indexes is at the last position of the nested lists in parameter_possible_values
        # while(sum(1 for x in range(len(idx_list)) if idx_list[x] == len(parameter_possible_values[x])-1 )
        #                     !=len(idx_list) ):
        #ABOVE complex check is not needed, see end of while loop
        while True:
            current_var_instantitations = [ parameter_possible_values[x][idx_list[x]] for x in range(len(idx_list))]
            var_mapping = dict(zip(parameter_keys,current_var_instantitations))
            # now with variable mapping, test if the translated preconditions which are static fluents are in the init state
            passed_static_precond = True
            for single_static_precondition in actionObj.static_preconditions_set:
                precond_parts = single_static_precondition.split("_")
                #we do NOT do a direct replace using the var to ground mapping, as the property type may match the variable, for example "OBJ obj"
                grounded_precond_parts = [precond_parts[0]] + [var_mapping[precond_parts[i]] for i in range(1,len(precond_parts)) ]
                grounded_precond = "_".join(grounded_precond_parts)
                if not grounded_precond in problem_parser_obj.fluents_set:
                    passed_static_precond = False
                    break
                #end if
            #end for through the static preconditions
            if passed_static_precond:
                valid_groundings.add(tuple(current_var_instantitations))
            #NOW update the indices to get the next possible instantiation.
            update_pos = -1
            while True:
                idx_list[update_pos] += 1
                if idx_list[update_pos] == len(parameter_possible_values[update_pos]):
                    idx_list[update_pos] = 0
                    update_pos -= 1
                #end if
                else:
                    break
                #end else
                if update_pos == -1*len(parameter_possible_values)-1: #we HAVE CHECKED ALL CASES
                    break
            #end while true updating the indices of grounding list
            if update_pos == -1 * len(parameter_possible_values) - 1:  # we HAVE CHECKED ALL CASES
                # return what we have
                break
        #end while loop checking for valid index
        return valid_groundings
    #=========================================================
    # =========================================================

    def generate_all_grounded_actions(self,problem_parser_obj):
        """
        :summary: using the objects and init state specified through the problem parser object, get all the grounded
        actions possible. All static fluents are checked against the initial state to see if it is true
        :param problem_parser_obj:
        :return:
        """
        grounded_actions_set = set()
        for single_action_name in self.actionObj_dict.keys():
            #get the parameter groundings
            groundings_set = self.get_all_parameter_groundings(single_action_name,problem_parser_obj)
            actionObj = self.actionObj_dict[single_action_name]
            #the variables in each grounding are in alphabetical order
            for curr_grounding in groundings_set:
                curr_action_data = []
                parameter_dict = actionObj.parameter_name_type_dict
                parameter_keys = sorted(list(parameter_dict.keys()))
                var_mapping = dict(zip(parameter_keys, curr_grounding))


                static_fluents = set()
                for single_fluent in actionObj.static_preconditions_set:
                    fluent_parts = single_fluent.split("_")
                    ground_fluent_parts = [fluent_parts[0]] + [var_mapping[fluent_parts[i]] for i in
                                                                   range(1, len(fluent_parts))]
                    static_fluents.add("_".join(ground_fluent_parts))

                for single_fluent in actionObj.preconditions_set:
                    fluent_parts = single_fluent.split("_")
                    ground_fluent_parts = [fluent_parts[0]] + [var_mapping[fluent_parts[i]] for i in
                                                                   range(1, len(fluent_parts))]
                    ground_fluent = "_".join(ground_fluent_parts)
                    if ground_fluent not in static_fluents:
                        curr_action_data.append(ground_fluent)
                #end for loop through preconditions
                #now add the action name
                curr_action_data.append("_".join(["ACTION",single_action_name] + list(curr_grounding)))  # first add the grounded action signature
                #finally add just the positive effects, (neg effects is duplicate information when things are in state variable format)
                for single_fluent in actionObj.pos_effects_set:
                    fluent_parts = single_fluent.split("_")
                    ground_fluent_parts = [fluent_parts[0]] + [var_mapping[fluent_parts[i]] for i in
                                                                   range(1, len(fluent_parts))]
                    ground_fluent = "_".join(ground_fluent_parts)
                    #check if it is not static, and the pos effect was not already true in the preconditions (poor spec)
                    if ground_fluent not in static_fluents and ground_fluent not in curr_action_data:
                        curr_action_data.append(ground_fluent)
                #end for loop through the positive effects
                grounded_actions_set.add(tuple(curr_action_data))
            #end for loop through the possible groundings for the aciton
        #end for loop through the actions in the domain
        return grounded_actions_set
    #end function generate_all_grounded_actions

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

class Problem_file_parser:

    class ProblemFile_parsing_state(Enum):
        no_section = 0
        in_objects = 1
        in_init = 2
        in_goal = 3


    def __init__(self, problem_file_loc):
        self.obj_dict = {}
        self.fluents_set = set()

        self.process_problem_file(problem_file_loc)


    def process_problem_file(self,problem_file_loc):
        """
        :summary: extract and set the obj dict and fluents set
        :param problem_file_loc:
        :return:
        """
        objects_start_token = ":object"
        init_start_token = ":init"
        goal_start_token = ":goal"
        parsing_state = self.ProblemFile_parsing_state.no_section

        with open(problem_file_loc,"r") as problem_file:
            for line_in_problem in problem_file:
                if line_in_problem.startswith(";"):
                    continue
                if objects_start_token in line_in_problem:
                    parsing_state = self.ProblemFile_parsing_state.in_objects
                elif init_start_token in line_in_problem:
                    parsing_state = self.ProblemFile_parsing_state.in_init
                elif goal_start_token in line_in_problem:
                    parsing_state = self.ProblemFile_parsing_state.in_goal
                elif parsing_state == self.ProblemFile_parsing_state.in_objects:
                    line_parts = line_in_problem.split("-")
                    if len(line_parts) < 2:#not a valid line
                        continue
                    object_mapping_values = line_parts[0].split(" ")
                    object_mapping_values = [x.lower() for x in object_mapping_values if x != '']
                    object_mapping_key = line_parts[1].strip().lower()
                    object_mapping_key = object_mapping_key.replace(")","")
                    self.obj_dict[object_mapping_key] = object_mapping_values
                    if ")" in line_in_problem:
                        parsing_state = self.ProblemFile_parsing_state.no_section
                elif parsing_state == self.ProblemFile_parsing_state.in_init:
                    line_in_problem = line_in_problem.replace(")","").replace("(","").replace("\n","")
                    if len(line_in_problem) < 3: #minimum is "a b" = <property><space><value>
                        continue
                    #end if
                    line_in_problem = line_in_problem.replace(" ","_")
                    self.fluents_set.add(line_in_problem.lower())
                elif parsing_state == self.ProblemFile_parsing_state.in_goal:
                    break
                #we are not processing the goal information yet
            #end for loop through lines in the file
        #end with statement keeping the file open
    #end function process file

#---end class problem file parser






# ==============================================================================+++
domain_parser_obj = Domain_manipulator(domain_file_loc)

#NOW go through the problem file, and build the dict of objects !
# AND all the fluents that are true at the start (this will include the static fluents

#parse problem file as well
problem_file_obj = Problem_file_parser(problem_file_loc)


all_actions = domain_parser_obj.generate_all_grounded_actions(problem_file_obj)

# with open(pickle_dest_file, "rb") as source_file:
#     all_solutions = pickle.load(source_file)


with open(pickle_dest_file, "wb") as destination:
    pickle.dump(all_actions, destination)

# testing code
with open(pickle_dest_file, "rb") as source_file:
    a = pickle.load(source_file)
    for single in a:
        print(single)


