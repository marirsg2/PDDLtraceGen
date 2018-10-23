(define (domain logistics-strips)
  (:requirements
                :strips)
  (:types
            tOBJ tTRUCK tLOCATION tCITY tAIRPLANE tAIRPLANEACCESS0 tAIRPLANEACCESS1 tAIRPLANEACCESS2 tAIRPLANEACCESS3 tAIRPORTACCESS0 tAIRPORTACCESS1 tAIRPORTACCESS2 tAIRPORTACCESS3- object
            tAIRPLANEACCESS0 tAIRPLANEACCESS1 tAIRPLANEACCESS2 tAIRPLANEACCESS3 - tAIRPLANE
            tAIRPORTACCESS0 tAIRPORTACCESS1 tAIRPORTACCESS2 tAIRPORTACCESS3 - tLOCATION )
  (:predicates
            (OBJ ?obj)
	       	(TRUCK ?truck)
               	(LOCATION ?loc)
        (AIRPLANE ?airplane)
		(AIRPLANEACCESS0 ?airplane)
		(AIRPLANEACCESS1 ?airplane)
		(AIRPLANEACCESS2 ?airplane)
		(AIRPLANEACCESS3 ?airplane)
                (CITY ?city)
                (AIRPORTACCESS0 ?airport)
                (AIRPORTACCESS1 ?airport)
                (AIRPORTACCESS2 ?airport)
                (AIRPORTACCESS3 ?airport)
		(in ?obj ?loc)
		(in ?obj1 ?obj2)
		(inCity ?obj ?city))

;IMPORTANT in-city is swapped to inCity. "-" is used as a special character and allowed in naming. This is a mistake for a language specification.
; ALSO IMPORTANT. loc-from and loc-to have been changed to locFrom and locTo. The "-" is used in other places such as object definition , as a language special character.
; this is a mistake on pddl specificaiton on what characters should be allowed in names.
; IMPORTANT do NOT use "_" in any naming

; ==================================================================================

(:action LOAD-TRUCK
  :parameters
   (?obj - tOBJ
    ?truck - tTRUCK
    ?loc - tLOCATION )
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
   (in ?truck ?loc) (in ?obj ?loc))
  :effect
   (and (not (in ?obj ?loc)) (in ?obj ?truck)))

(:action LOAD-AIRPLANE
  :parameters
   (?obj - tOBJ
    ?airplane - tAIRPLANE
    ?loc - tLOCATION )
  :precondition
   (and (OBJ ?obj) (AIRPLANE ?airplane) (LOCATION ?loc)
   (in ?obj ?loc) (in ?airplane ?loc))
  :effect
   (and (not (in ?obj ?loc)) (in ?obj ?airplane)))

(:action UNLOAD-TRUCK
  :parameters
   (?obj - tOBJ
    ?truck - tTRUCK
    ?loc - tLOCATION)
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
        (in ?truck ?loc) (in ?obj ?truck))
  :effect
   (and (not (in ?obj ?truck)) (in ?obj ?loc)))

(:action UNLOAD-AIRPLANE
  :parameters
   (?obj - tOBJ
    ?airplane - tAIRPLANE
    ?loc - tLOCATION )
  :precondition
   (and (OBJ ?obj) (AIRPLANE ?airplane) (LOCATION ?loc)
        (in ?obj ?airplane) (in ?airplane ?loc))
  :effect
   (and (not (in ?obj ?airplane)) (in ?obj ?loc)))

(:action DRIVE-TRUCK
  :parameters
   (?truck - tTRUCK
    ?locFrom - tLOCATION
    ?locTo - tLOCATION
    ?city - tCITY )
  :precondition
   (and (TRUCK ?truck) (LOCATION ?locFrom) (LOCATION ?locTo) (CITY ?city)
   (in ?truck ?locFrom)
   (inCity ?locFrom ?city)
   (inCity ?locTo ?city))
  :effect
   (and (not (in ?truck ?locFrom)) (in ?truck ?locTo)))

;=======================================================
; The different fly actions for different access regions

(:action FLY-AIRPLANEACCESS0
  :parameters
   (?airplane - tAIRPLANEACCESS0
    ?locFrom - tAIRPORTACCESS0
    ?locTo - tAIRPORTACCESS0 )
  :precondition
   (and (AIRPLANEACCESS0 ?airplane) (AIRPORTACCESS0 ?locFrom) (AIRPORTACCESS0 ?locTo)
	(in ?airplane ?locFrom))
  :effect
   (and (not (in ?airplane ?locFrom)) (in ?airplane ?locTo)))

(:action FLY-AIRPLANEACCESS1
  :parameters
   (?airplane - tAIRPLANEACCESS1
    ?locFrom - tAIRPORTACCESS1
    ?locTo - tAIRPORTACCESS1 )
  :precondition
   (and (AIRPLANEACCESS1 ?airplane) (AIRPORTACCESS1 ?locFrom) (AIRPORTACCESS1 ?locTo)
	(in ?airplane ?locFrom))
  :effect
   (and (not (in ?airplane ?locFrom)) (in ?airplane ?locTo)))


(:action FLY-AIRPLANEACCESS2
  :parameters
   (?airplane - tAIRPLANEACCESS2
    ?locFrom - tAIRPORTACCESS2
    ?locTo - tAIRPORTACCESS2 )
  :precondition
   (and (AIRPLANEACCESS2 ?airplane) (AIRPORTACCESS2 ?locFrom) (AIRPORTACCESS2 ?locTo)
	(in ?airplane ?locFrom))
  :effect
   (and (not (in ?airplane ?locFrom)) (in ?airplane ?locTo)))


(:action FLY-AIRPLANEACCESS3
  :parameters
   (?airplane - tAIRPLANEACCESS3
    ?locFrom - tAIRPORTACCESS3
    ?locTo - tAIRPORTACCESS3 )
  :precondition
   (and (AIRPLANEACCESS3 ?airplane) (AIRPORTACCESS3 ?locFrom) (AIRPORTACCESS3 ?locTo)
	(in ?airplane ?locFrom))
  :effect
   (and (not (in ?airplane ?locFrom)) (in ?airplane ?locTo)))


) ; END OF DOMAIN FILE
