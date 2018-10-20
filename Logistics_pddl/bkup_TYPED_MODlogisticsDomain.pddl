(define (domain logistics-strips)
  (:requirements :strips)
  (:types OBJ TRUCK LOCATION AIRPLANE AIRPLANE_ACCESS0 AIRPLANE_ACCESS1 AIRPLANE_ACCESS2 AIRPLANE_ACCESS3 AIRPORT_ACCESS0 AIRPORT_ACCESS1 AIRPORT_ACCESS2 AIRPORT_ACCESS3- object)
  (:predicates 	(OBJ ?obj)
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
		(at ?obj ?loc)
		(in ?obj1 ?obj2)
		(in-city ?obj ?city))
 
  ; (:types )		; default object

; #<class 'tuple'>: ('drive-truck_t1_l12_l10_c1', 'load-truck_p0_t1_l10', 'drive-truck_t1_l10_l11_c1', 'unload-truck_p0_t1_l11')

(:action LOAD-TRUCK
  :parameters
   (?obj - OBJ
    ?truck - TRUCK
    ?loc - LOCATION )
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
   (at ?truck ?loc) (at ?obj ?loc))
  :effect
   (and (not (at ?obj ?loc)) (in ?obj ?truck)))

(:action LOAD-AIRPLANE
  :parameters
   (?obj - OBJ
    ?airplane - AIRPLANE
    ?loc - LOCATION )
  :precondition
   (and (OBJ ?obj) (AIRPLANE ?airplane) (LOCATION ?loc)
   (at ?obj ?loc) (at ?airplane ?loc))
  :effect
   (and (not (at ?obj ?loc)) (in ?obj ?airplane)))

(:action UNLOAD-TRUCK
  :parameters
   (?obj - OBJ
    ?truck - TRUCK
    ?loc - LOCATION)
  :precondition
   (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
        (at ?truck ?loc) (in ?obj ?truck))
  :effect
   (and (not (in ?obj ?truck)) (at ?obj ?loc)))

(:action UNLOAD-AIRPLANE
  :parameters
   (?obj - OBJ
    ?airplane - AIRPLANE
    ?loc - LOCATION )
  :precondition
   (and (OBJ ?obj) (AIRPLANE ?airplane) (LOCATION ?loc)
        (in ?obj ?airplane) (at ?airplane ?loc))
  :effect
   (and (not (in ?obj ?airplane)) (at ?obj ?loc)))

(:action DRIVE-TRUCK
  :parameters
   (?truck - TRUCK
    ?loc-from - LOCATION
    ?loc-to - LOCATION
    ?city - CITY )
  :precondition
   (and (TRUCK ?truck) (LOCATION ?loc-from) (LOCATION ?loc-to) (CITY ?city)
   (at ?truck ?loc-from)
   (in-city ?loc-from ?city)
   (in-city ?loc-to ?city))
  :effect
   (and (not (at ?truck ?loc-from)) (at ?truck ?loc-to)))

;=======================================================
; The different fly actions for different access regions

(:action FLY-AIRPLANE_ACCESS0
  :parameters
   (?airplane - AIRPLANE_ACCESS0
    ?loc-from - AIRPORT_ACCESS0
    ?loc-to - AIRPORT_ACCESS0 )
  :precondition
   (and (AIRPLANE_ACCESS0 ?airplane) (AIRPORT_ACCESS0 ?loc-from) (AIRPORT_ACCESS0 ?loc-to)
	(at ?airplane ?loc-from))
  :effect
   (and (not (at ?airplane ?loc-from)) (at ?airplane ?loc-to)))

(:action FLY-AIRPLANE_ACCESS1
  :parameters
   (?airplane - AIRPLANE_ACCESS1
    ?loc-from - AIRPORT_ACCESS1
    ?loc-to - AIRPORT_ACCESS1 )
  :precondition
   (and (AIRPLANE_ACCESS1 ?airplane) (AIRPORT_ACCESS1 ?loc-from) (AIRPORT_ACCESS1 ?loc-to)
	(at ?airplane ?loc-from))
  :effect
   (and (not (at ?airplane ?loc-from)) (at ?airplane ?loc-to)))


(:action FLY-AIRPLANE_ACCESS2
  :parameters
   (?airplane - AIRPLANE_ACCESS2
    ?loc-from - AIRPORT_ACCESS2
    ?loc-to - AIRPORT_ACCESS2 )
  :precondition
   (and (AIRPLANE_ACCESS2 ?airplane) (AIRPORT_ACCESS2 ?loc-from) (AIRPORT_ACCESS2 ?loc-to)
	(at ?airplane ?loc-from))
  :effect
   (and (not (at ?airplane ?loc-from)) (at ?airplane ?loc-to)))


(:action FLY-AIRPLANE_ACCESS3
  :parameters
   (?airplane - AIRPLANE_ACCESS3
    ?loc-from - AIRPORT_ACCESS3
    ?loc-to - AIRPORT_ACCESS3 )
  :precondition
   (and (AIRPLANE_ACCESS3 ?airplane) (AIRPORT_ACCESS3 ?loc-from) (AIRPORT_ACCESS3 ?loc-to)
	(at ?airplane ?loc-from))
  :effect
   (and (not (at ?airplane ?loc-from)) (at ?airplane ?loc-to)))


) ; END OF DOMAIN FILE
