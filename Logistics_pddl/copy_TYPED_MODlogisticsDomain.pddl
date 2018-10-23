(define (domain logistics-strips)
  (:requirements
                :strips)
  (:types tOBJ
                tTRUCK tLOCATION tCITY tAIRPLANE tAIRPLANE_ACCESS0 tAIRPLANE_ACCESS1 tAIRPLANE_ACCESS2 tAIRPLANE_ACCESS3 tAIRPORT_ACCESS0 tAIRPORT_ACCESS1 tAIRPORT_ACCESS2 tAIRPORT_ACCESS3- object
                tAIRPLANE_ACCESS0 tAIRPLANE_ACCESS1 tAIRPLANE_ACCESS2 tAIRPLANE_ACCESS3 - tAIRPLANE
                tAIRPORT_ACCESS0 tAIRPORT_ACCESS1 tAIRPORT_ACCESS2 tAIRPORT_ACCESS3 - tLOCATION )
  (:predicates
            (OBJ ?obj)
	       	(TRUCK ?truck)
               	(LOCATION ?loc)
        (AIRPLANE ?airplane)
		(AIRPLANE_ACCESS0 ?airplane)
		(AIRPLANE_ACCESS1 ?airplane)
		(AIRPLANE_ACCESS2 ?airplane)
		(AIRPLANE_ACCESS3 ?airplane)
                (CITY ?city)
                (AIRPORT_ACCESS0 ?airport)
                (AIRPORT_ACCESS1 ?airport)
                (AIRPORT_ACCESS2 ?airport)
                (AIRPORT_ACCESS3 ?airport)
		(in ?obj ?loc)
		(in ?obj1 ?obj2)
		(in-city ?obj ?city))
 
  ; (:types )		; default object

; #<class 'tuple'>: ('drive-truck_t1_l12_l10_c1', 'load-truck_p0_t1_l10', 'drive-truck_t1_l10_l11_c1', 'unload-truck_p0_t1_l11')

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

(:action FLY-AIRPLANE_ACCESS0
  :parameters
   (?airplane - tAIRPLANE_ACCESS0
    ?loc-from - tAIRPORT_ACCESS0
    ?loc-to - tAIRPORT_ACCESS0 )
  :precondition
   (and (AIRPLANE_ACCESS0 ?airplane) (AIRPORT_ACCESS0 ?loc-from) (AIRPORT_ACCESS0 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))

(:action FLY-AIRPLANE_ACCESS1
  :parameters
   (?airplane - tAIRPLANE_ACCESS1
    ?loc-from - tAIRPORT_ACCESS1
    ?loc-to - tAIRPORT_ACCESS1 )
  :precondition
   (and (AIRPLANE_ACCESS1 ?airplane) (AIRPORT_ACCESS1 ?loc-from) (AIRPORT_ACCESS1 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))


(:action FLY-AIRPLANE_ACCESS2
  :parameters
   (?airplane - tAIRPLANE_ACCESS2
    ?loc-from - tAIRPORT_ACCESS2
    ?loc-to - tAIRPORT_ACCESS2 )
  :precondition
   (and (AIRPLANE_ACCESS2 ?airplane) (AIRPORT_ACCESS2 ?loc-from) (AIRPORT_ACCESS2 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))


(:action FLY-AIRPLANE_ACCESS3
  :parameters
   (?airplane - tAIRPLANE_ACCESS3
    ?loc-from - tAIRPORT_ACCESS3
    ?loc-to - tAIRPORT_ACCESS3 )
  :precondition
   (and (AIRPLANE_ACCESS3 ?airplane) (AIRPORT_ACCESS3 ?loc-from) (AIRPORT_ACCESS3 ?loc-to)
	(in ?airplane ?loc-from))
  :effect
   (and (not (in ?airplane ?loc-from)) (in ?airplane ?loc-to)))


) ; END OF DOMAIN FILE
