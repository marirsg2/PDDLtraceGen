"""
Sample
(define (problem BW-rand-50)
(:domain blocksworld)
(:objects b1 b2 b3 - block)
(:init
(handempty)
(ontable b1)
(on b3 b2)
(ontable b2)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
)
)
)
"""
import random
import copy
#================================================
def generate_problem(num_blocks, dest_file_name, num_blocks_in_goal = None):
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
    with open(dest_file_name,"w") as dest_file:
        dest_file.write("(define (problem BW-rand-" + str(num_blocks)+")\n")
        dest_file.write("(:domain blocksworld)\n")
        dest_file.write("(:objects " + " ".join(block_obj_list) + " - block)\n")
        dest_file.write("(:init \n")
        dest_file.write("")
        dest_file.write("(handempty)\n")
        for block in block_obj_list:
            #either choose a clear block to stack on, or be on table
            available_choices = clear_blocks + ["ontable"]
            pos = random.choice(available_choices)
            if pos == 'ontable':
                dest_file.write("(ontable "+block+")\n")
            else:#it will be placed on a block
                dest_file.write("(on "+block +' '+pos+")\n")
                clear_blocks.remove(pos)
        #end for loop
        dest_file.write(")\n")
        #now write the goals
        dest_file.write("(:goal\n")
        dest_file.write("(and\n")
        clear_blocks = copy.deepcopy(goal_blocks_list)
        for block in goal_blocks_list:
            #either choose a clear block to stack on, or be on table
            available_choices = clear_blocks+ ["ontable"]
            pos = random.choice(available_choices)
            if pos == 'ontable':
                dest_file.write("(ontable "+block+")\n")
            else:#it will be placed on a block
                dest_file.write("(on "+block +' '+pos+")\n")
                clear_blocks.remove(pos)
        #end for loop through goal blocks
        dest_file.write(")\n)\n)")
    #end with statement

if __name__ == "__main__":
    random.seed(4)
    generate_problem(5,"test_blocks_prob.pddl",3)