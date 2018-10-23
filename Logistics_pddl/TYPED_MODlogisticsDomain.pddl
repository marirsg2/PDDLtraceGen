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
		(in-city ?obj ?city))
 

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
    ?loc-from - tLOCATION
    ?loc-to - tLOCATION
    ?city - tCITY )
  :precondition
   (and (TRUCK ?truck) (LOCATION ?loc-from) (LOCATION ?loc-to) (CITY ?city)
   (in ?truck ?loc-from)
   (in-city ?loc-from ?city)
   (in-city ?loc-to ?city))
  :effect
   (and (not (in ?truck ?loc-from)) (in ?truck ?loc-to)))

;=======================================================
; The different fly actions for different access regions

(:action FLY-AIRPLANEACCESS0
  :parameters
   (?airplane - tAIRPLANEACCESS0
    ?loc-from - tAIRPORTACCESS0
    ?loc-to - tAIRPORTACCESS0 )
  :precondition
   (and (AIRPLANEACCESS0 ?airplane) (AIRPORTACCESS0 ?loc-from) (AIRPORTACCESS0 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))

(:action FLY-AIRPLANEACCESS1
  :parameters
   (?airplane - tAIRPLANEACCESS1
    ?loc-from - tAIRPORTACCESS1
    ?loc-to - tAIRPORTACCESS1 )
  :precondition
   (and (AIRPLANEACCESS1 ?airplane) (AIRPORTACCESS1 ?loc-from) (AIRPORTACCESS1 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))


(:action FLY-AIRPLANEACCESS2
  :parameters
   (?airplane - tAIRPLANEACCESS2
    ?loc-from - tAIRPORTACCESS2
    ?loc-to - tAIRPORTACCESS2 )
  :precondition
   (and (AIRPLANEACCESS2 ?airplane) (AIRPORTACCESS2 ?loc-from) (AIRPORTACCESS2 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))


(:action FLY-AIRPLANEACCESS3
  :parameters
   (?airplane - tAIRPLANEACCESS3
    ?loc-from - tAIRPORTACCESS3
    ?loc-to - tAIRPORTACCESS3 )
  :precondition
   (and (AIRPLANEACCESS3 ?airplane) (AIRPORTACCESS3 ?loc-from) (AIRPORTACCESS3 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))


) ; END OF DOMAIN FILE
