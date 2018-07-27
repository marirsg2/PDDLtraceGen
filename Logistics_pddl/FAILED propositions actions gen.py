
import pddlpy as pddl_parser

domain_file_loc = "./domain.pddl"
problem_file_loc = "./problem_logistics_c4_s3_p1_a1.pddl"

pddl_obj = pddl_parser.DomainProblem(domain_file_loc, problem_file_loc)

print(pddl_obj.initialstate())
a = pddl_obj.initialstate()
print(pddl_obj.operators())
print(list(pddl_obj.ground_operator("DRIVE-TRUCK")))