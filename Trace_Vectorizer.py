"""
:summary: This script converts traces of PDDL into vectorized state-sequences
Propositions are converted into binary dimensions, and numeric fluents are converted into float32 dimensions in the vector
"""

"""


Input is the starting full state and action traces. The domain model is also given.
Output is the vectorized form of all the action traces. 
Algorithm:
 Go through all the traces and build the vocabulary of propositions and fluents, define their vector position in a dictionary
 then vectorize each state . Every successive state is determined using the PDDL model of the domain

"""

#is there a way to get the full state with every step in pddl.