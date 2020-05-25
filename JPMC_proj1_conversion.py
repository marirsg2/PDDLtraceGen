"""
This code converts to the format

goal indices, **, action indices
goal fluents have separate indexing than actions


This is for logistics, so packages are goals
"""

#for each action, get the pair, then take the diff, these are the fluents that are changed. Assign indices to the fluents,
#todo track the goal fluents by looking for "at_p". In the second of the pair, is their final value per action.
# have a dict, the key is the prefix at_p0, at_p1, the value is the location. Keep updating when found. The final values are the goals

import pickle

source_pickle_file = "10000c10_s4_p10_a1_logistics_dataset.p"
all_solutions = []
with open(source_pickle_file, "rb") as src:
    all_solutions = pickle.load(src)

action_to_idx_list_map= []
fluent_to_idx_list_map= []
for single_goal,single_solution in all_solutions:

    solution_idx_form = []
    solution_readable_form = []
    goal_dict = {}
    for step_idx in range(0,len(single_solution),2):
        curr_action = single_solution[step_idx][-1]
        solution_readable_form.append(curr_action)
        try:
            solution_idx_form.append(action_to_idx_list_map.index(curr_action))
        except ValueError:
            action_to_idx_list_map.append(curr_action)
            solution_idx_form.append(action_to_idx_list_map.index(curr_action))
        prior_state = set(single_solution[step_idx])
        post_state = set(single_solution[step_idx+1])
        diff_state = post_state.difference(prior_state)
        for fluent in diff_state:
            if fluent.startswith("at_p"):
                variable_name = "_".join(fluent.split("_")[:-1])
                variable_value = fluent.split("_")[-1]
                goal_dict[variable_name] = variable_value
        #end for loop
    #end for loop through steps in a plan
    goal_readable_form = ["_".join(x) for x in goal_dict.items()]
    goal_idx_form = []
    for goal in goal_readable_form:
        try:
            goal_idx_form.append(fluent_to_idx_list_map.index(goal))
        except ValueError:
            fluent_to_idx_list_map.append(goal)
            goal_idx_form.append(fluent_to_idx_list_map.index(goal))

    print(solution_readable_form)
    print(solution_idx_form)
    print(goal_readable_form)
    print(goal_idx_form)
    print("==================")

#end for loop through all solutions(plans)




