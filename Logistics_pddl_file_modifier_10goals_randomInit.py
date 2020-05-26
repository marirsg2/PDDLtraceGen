"""
Given logistic pddl files makes some modifications and return it

"""
import random
import pickle

# Independent variables:
# - domain: blocks words, logistics, grid, ?
# - number of goals: \textbf{small} (2/3), large (10)
# - closeness of goals: \textbf{T} or F
# - length of prefix: short (< 5 actions), \textbf{long (> 5 actions)}
# - probability distributions on goals: uniform, \textbf{skewed (80/20)}
# - fixed initial state: \textbf{T} or F
# - planner: optimal vs \textbf{suboptimal}
# 

#todo LAMA FIRST

ten_goal_states_list = [

['(at p0 l10)\n',
'(at p1 l12)\n',
'(at p2 l12)\n',
'(at p3 l12)\n',
'(at p4 l12)\n',
'(at p5 l12)\n',
'(at p6 l12)\n',
'(at p7 l12)\n',
'(at p8 l12)\n',
'(at p9 l12)\n',],

['(at p0 l12)\n',
'(at p1 l12)\n',
'(at p2 l12)\n',
'(at p3 l12)\n',
'(at p4 l12)\n',
'(at p5 l12)\n',
'(at p6 l12)\n',
'(at p7 l12)\n',
'(at p8 l12)\n',
'(at p9 l12)\n',],
    
    ['(at p0 l20)\n',
'(at p1 l22)\n',
'(at p2 l22)\n',
'(at p3 l22)\n',
'(at p4 l22)\n',
'(at p5 l22)\n',
'(at p6 l22)\n',
'(at p7 l22)\n',
'(at p8 l22)\n',
'(at p9 l22)\n',],

['(at p0 l22)\n',
'(at p1 l22)\n',
'(at p2 l22)\n',
'(at p3 l22)\n',
'(at p4 l22)\n',
'(at p5 l22)\n',
'(at p6 l22)\n',
'(at p7 l22)\n',
'(at p8 l22)\n',
'(at p9 l22)\n',],
    
['(at p0 l30)\n',
'(at p1 l32)\n',
'(at p2 l32)\n',
'(at p3 l32)\n',
'(at p4 l32)\n',
'(at p5 l32)\n',
'(at p6 l32)\n',
'(at p7 l32)\n',
'(at p8 l32)\n',
'(at p9 l32)\n',],

['(at p0 l32)\n',
'(at p1 l32)\n',
'(at p2 l32)\n',
'(at p3 l32)\n',
'(at p4 l32)\n',
'(at p5 l32)\n',
'(at p6 l32)\n',
'(at p7 l32)\n',
'(at p8 l32)\n',
'(at p9 l32)\n',],

['(at p0 l40)\n',
'(at p1 l42)\n',
'(at p2 l42)\n',
'(at p3 l42)\n',
'(at p4 l42)\n',
'(at p5 l42)\n',
'(at p6 l42)\n',
'(at p7 l42)\n',
'(at p8 l42)\n',
'(at p9 l42)\n',],

['(at p0 l42)\n',
'(at p1 l42)\n',
'(at p2 l42)\n',
'(at p3 l42)\n',
'(at p4 l42)\n',
'(at p5 l42)\n',
'(at p6 l42)\n',
'(at p7 l42)\n',
'(at p8 l42)\n',
'(at p9 l42)\n',],

['(at p0 l50)\n',
'(at p1 l52)\n',
'(at p2 l52)\n',
'(at p3 l52)\n',
'(at p4 l52)\n',
'(at p5 l52)\n',
'(at p6 l52)\n',
'(at p7 l52)\n',
'(at p8 l52)\n',
'(at p9 l52)\n',],

['(at p0 l52)\n',
'(at p1 l52)\n',
'(at p2 l52)\n',
'(at p3 l52)\n',
'(at p4 l52)\n',
'(at p5 l52)\n',
'(at p6 l52)\n',
'(at p7 l52)\n',
'(at p8 l52)\n',
'(at p9 l52)\n',],

]



# def edit_initial_state_10goals_randomInit(source_problem_file):
#     #read the problem file, and drop all lines that contain '(at p'. note the index where the first 'at p' occurs (initial state)
#     #and the index where the goal fluents start
#     #fill in the replacements at those indices.
#     all_lines = []
#     with open(source_problem_file,"r") as src_problem_pddl:
#         all_lines = src_problem_pddl.readlines()
#     goal_state_idx = all_lines.index("(and\n")
#     necessary_lines_after_goal_start = [x for x in all_lines[goal_state_idx+1:] if "at p" not in x ]
#
#     goal_state_probability = random.random()
#     goal_state_selection_idx = int(goal_state_probability*10)
#     goal_state_fluents = ten_goal_states_list[goal_state_selection_idx]
#     #end if
#     all_lines = all_lines[0:goal_state_idx+1] + goal_state_fluents + necessary_lines_after_goal_start
#     with open(source_problem_file,"w") as dest_problem_pddl:
#         dest_problem_pddl.writelines(all_lines)
#     return goal_state_fluents
# #end function edit initial state

def edit_initial_state_and_get_goal_and_template_10goals_randomInit(source_problem_file):
    #read the problem file, and drop all lines that contain '(at p'. note the index where the first 'at p' occurs (initial state)
    #and the index where the goal fluents start
    #fill in the replacements at those indices.
    all_lines = []
    template_lines = []
    with open(source_problem_file,"r") as src_problem_pddl:
        all_lines = src_problem_pddl.readlines()

    goal_state_idx = all_lines.index("(and\n")
    necessary_lines_after_goal_start = [x for x in all_lines[goal_state_idx+1:] if "at p" not in x ]
    template_lines = all_lines[0:goal_state_idx+1] + ["<HYPOTHESIS>\n"] + necessary_lines_after_goal_start

    goal_state_probability = random.random()
    goal_state_selection_idx = int(goal_state_probability*10)
    goal_state_fluents = ten_goal_states_list[goal_state_selection_idx]
    #end if
    all_lines = all_lines[0:goal_state_idx+1] + goal_state_fluents + necessary_lines_after_goal_start
    with open(source_problem_file,"w") as dest_problem_pddl:
        dest_problem_pddl.writelines(all_lines)
    return goal_state_fluents,template_lines
#end function edit initial state

