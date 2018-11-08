;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 Op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain BLOCKS)
  (:requirements :strips)
  (:types
            tblock thand ttable- object
            )
  (:predicates
           (onblock ?x ?y)
           (onblock ?x noblock)
           (under ?x ?y)
           (under ?x none)
	       (holding ?x ?y)
	       (holding ?x nothing)
	       (ontable ?x ?y)
	       (ontable ?x notable)

	       )

  (:action pick-up
	     :parameters
	     (?b - tblock
	      ?h - thand
	      ?t - ttable)
	     :precondition (and (under ?b none) (ontable ?b ?t) (holding ?h nothing))
	     :effect
	     (and (not (ontable ?b ?t))
		   (not (holding ?h nothing))
		   (holding ?h ?b)))


   ; ===========  INCOMPLETE !! FINISH THE OTHER ACTIONS

  (:action put-down
	     :parameters
	     (?b - tblock
	      ?h - thand
	      ?t - ttable)
	     :precondition (and (holding ?h ?b))
	     :effect
	     (and (not(holding ?h ?b))
	       (carrying ?t ?b)
		   (holding ?h nothing)))




  (:action stack
	     :parameters
	     (?x - tblock
	      ?y - tblock)
	     :precondition (and (holding ?x) (clear ?y))
	     :effect
	     (and (not (holding ?x))
		   (not (clear ?y))
		   (clear ?x)
		   (handempty)
		   (on ?x ?y)))
  (:action unstack
	     :parameters
	     (?x - tblock
	      ?y - tblock)
	     :precondition (and (on ?x ?y) (clear ?x) (handempty))
	     :effect
	     (and (holding ?x)
		   (clear ?y)
		   (not (clear ?x))
		   (not (handempty))
		   (not (on ?x ?y)))))
