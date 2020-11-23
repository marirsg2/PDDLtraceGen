(define (domain gripper-strips)
    (:requirements :strips :typing) 
  (:types robot room ball gripper - object)
  (:predicates (at-robby ?r - robot ?ro - room)
	       (at ?b - ball ?r - room)
	       (free ?r - robot ?g - gripper)
	       (carry ?b - ball ?g - gripper))

  (:action move
	   :parameters (?r - robot ?from - room ?to - room)
	   :precondition (and (at-robby ?r ?from))
	   :effect (and (at-robby ?r ?to)
			(not (at-robby ?r ?from))))

  (:action pick
	   :parameters (?r - robot ?obj - ball ?room - room ?gripper - gripper)
	   :precondition (and (at ?obj ?room) (at-robby ?r ?room) (free ?r ?gripper))
	   :effect (and (carry ?obj ?gripper)
			(not (at ?obj ?room)) 
			(not (free ?r ?gripper))))

  (:action drop
	   :parameters (?r - robot ?obj - ball ?room - room ?gripper - gripper)
	   :precondition (and (carry ?obj ?gripper) (at-robby ?r ?room))
	   :effect (and (at ?obj ?room)
			(free ?r ?gripper)
			(not (carry ?obj ?gripper)))))

