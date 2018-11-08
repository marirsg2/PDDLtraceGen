(define (domain logistics-strips)
  (:requirements
                :strips)
  (:types
            tOBJ tTRUCK tLOCATION tCITY tAIRPLANE - object
            )
  (:predicates
        (OBJ ?obj)
        (TRUCK ?truck)
        (LOCATION ?loc)
        (AIRPLANE ?airplane)
        (CITY ?city)
        (AIRPORT ?loc)
		(in ?obj ?loc)
		(in ?obj1 ?obj2)
		(inCity ?obj ?city)
		(drivesInside ?truck ?city)
		(fliesTo ?airplane ?location)
		)

;IMPORTANT in-city is swapped to inCity. "-" is used as a special character and allowed in naming. This is a mistake for a language specification.
; ALSO IMPORTANT. locFrom and locTo have been changed to locFrom and locTo. The "-" is used in other places such as object definition , as a language special character.
; this is a mistake on pddl specification on what characters should be allowed in names.
; IMPORTANT do NOT use "_" in any naming
; IMPORTANT put the action parameters in alphabetical ascending order of their variable names
; IMPORTANT sadly the code is not robust, and so in the action parameter list, as soon as you open bracket, you need a parameter in the same line i.e.
; do ""(?var - type" not "( \n ?var - type"
; ==================================================================================

(:action LOAD-TRUCK
  :parameters
   (?city - tCity
    ?loc - tLOCATION
    ?obj - tOBJ
    ?truck - tTRUCK)
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc) (CITY ?city)
   (in ?truck ?loc) (in ?obj ?loc)
   (inCity ?loc ?city)(drivesInside ?truck ?city))
  :effect
   (and (not (in ?obj ?loc)) (in ?obj ?truck)))


(:action LOAD-AIRPLANE
  :parameters
   (?airplane - tAIRPLANE
    ?loc - tLOCATION
    ?obj - tOBJ)
  :precondition
  (and (OBJ ?obj) (AIRPLANE ?airplane) (AIRPORT ?loc)
   (in ?obj ?loc) (in ?airplane ?loc)
   (fliesTo ?airplane ?loc))
  :effect
   (and (not (in ?obj ?loc)) (in ?obj ?airplane)))

(:action UNLOAD-TRUCK
  :parameters
   (?city - tCITY
    ?loc - tLOCATION
    ?obj - tOBJ
    ?truck - tTRUCK)
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc) (CITY ?city)
    (in ?truck ?loc) (in ?obj ?truck)
    (inCity ?loc ?city)(drivesInside ?truck ?city))
  :effect
   (and (not (in ?obj ?truck)) (in ?obj ?loc)))

(:action UNLOAD-AIRPLANE
  :parameters
   (?airplane - tAIRPLANE
    ?loc - tLOCATION
    ?obj - tOBJ)
  :precondition
   (and (OBJ ?obj) (AIRPLANE ?airplane) (AIRPORT ?loc)
        (in ?obj ?airplane) (in ?airplane ?loc)
       (fliesTo ?airplane ?loc) )
  :effect
   (and (not (in ?obj ?airplane)) (in ?obj ?loc)))

(:action DRIVE-TRUCK
  :parameters
   (?city - tCITY
    ?locFrom - tLOCATION
    ?locTo - tLOCATION
    ?truck - tTRUCK)
  :precondition
   (and (TRUCK ?truck) (LOCATION ?locFrom) (LOCATION ?locTo) (CITY ?city)
   (in ?truck ?locFrom)
   (inCity ?locFrom ?city)
   (inCity ?locTo ?city)
   (drivesInside ?truck ?city))
  :effect
   (and (not (in ?truck ?locFrom)) (in ?truck ?locTo)))

(:action FLY-AIRPLANE
  :parameters
   (?airplane - tAIRPLANE
    ?locFrom - tLOCATION
    ?locTo - tLOCATION)
  :precondition
   (and (AIRPLANE ?airplane) (AIRPORT ?locFrom) (AIRPORT ?locTo)
	(in ?airplane ?locFrom)
	(fliesTo ?airplane ?locFrom)
	(fliesTo ?airplane ?locTo))
  :effect
   (and (not (in ?airplane ?locFrom)) (in ?airplane ?locTo)))

) ; END OF DOMAIN FILE

