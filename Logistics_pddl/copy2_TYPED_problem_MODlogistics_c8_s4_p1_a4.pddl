


(define (problem logistics-c8-s4-p1-a4)
(:domain logistics-strips)
(:objects
          c0 c1 c2 c3 c4 c5 c6 c7 - tCITY
          t0 t1 t2 t3 t4 t5 t6 t7 - tTRUCK
          l01 l02 l03 l11 l12 l13 l21 l22 l23 l31 l32 l41 l42 l51 l52 l61 l62 l71 l72 l73 - tLOCATION
          p0 - tOBJ
          a0 - tAIRPLANEACCESS0
          a1 - tAIRPLANEACCESS1
          a2 - tAIRPLANEACCESS2
          a3 - tAIRPLANEACCESS3
          l00 l10 l20 l30 - tAIRPORTACCESS0
                  l43 l33 - tAIRPORTACCESS1
              l40 l50 l60 - tAIRPORTACCESS2
              l70 l53 l63 - tAIRPORTACCESS3
)
; The major modification is that the airplanes are both regular airplanes (for loading and unloading) as well as special airplanes for accessing specific
; subset of cities. This separates the cities.
; a0 a1 a2 a3 - tAIRPLANE
;IMPORTANT in-city is swapped to inCity. "-" is used as a special character and allowed in naming. This is a mistake for a language specification.
; IMPORTANT do NOT use "_" in any naming

(:init
(AIRPLANE a0)
(AIRPLANE a1)
(AIRPLANE a2)
(AIRPLANE a3)
(AIRPLANEACCESS0 a0)
(AIRPLANEACCESS1 a1)
(AIRPLANEACCESS2 a2)
(AIRPLANEACCESS3 a3)
(CITY c0)
(CITY c1)
(CITY c2)
(CITY c3)
(CITY c4)
(CITY c5)
(CITY c6)
(CITY c7)
(TRUCK t0)
(TRUCK t1)
(TRUCK t2)
(TRUCK t3)
(TRUCK t4)
(TRUCK t5)
(TRUCK t6)
(TRUCK t7)
(LOCATION l00)
(inCity  l00 c0)
(LOCATION l01)
(inCity  l01 c0)
(LOCATION l02)
(inCity  l02 c0)
(LOCATION l03)
(inCity  l03 c0)
(LOCATION l10)
(inCity  l10 c1)
(LOCATION l11)
(inCity  l11 c1)
(LOCATION l12)
(inCity  l12 c1)
(LOCATION l13)
(inCity  l13 c1)
(LOCATION l20)
(inCity  l20 c2)
(LOCATION l21)
(inCity  l21 c2)
(LOCATION l22)
(inCity  l22 c2)
(LOCATION l23)
(inCity  l23 c2)
(LOCATION l30)
(inCity  l30 c3)
(LOCATION l31)
(inCity  l31 c3)
(LOCATION l32)
(inCity  l32 c3)
(LOCATION l33)
(inCity  l33 c3)
(LOCATION l40)
(inCity  l40 c4)
(LOCATION l41)
(inCity  l41 c4)
(LOCATION l42)
(inCity  l42 c4)
(LOCATION l43)
(inCity  l43 c4)
(LOCATION l50)
(inCity  l50 c5)
(LOCATION l51)
(inCity  l51 c5)
(LOCATION l52)
(inCity  l52 c5)
(LOCATION l53)
(inCity  l53 c5)
(LOCATION l60)
(inCity  l60 c6)
(LOCATION l61)
(inCity  l61 c6)
(LOCATION l62)
(inCity  l62 c6)
(LOCATION l63)
(inCity  l63 c6)
(LOCATION l70)
(inCity  l70 c7)
(LOCATION l71)
(inCity  l71 c7)
(LOCATION l72)
(inCity  l72 c7)
(LOCATION l73)
(inCity  l73 c7)
(AIRPORTACCESS0 l00)
(AIRPORTACCESS0 l10)
(AIRPORTACCESS0 l20)
(AIRPORTACCESS0 l30)

(AIRPORTACCESS1 l33)
(AIRPORTACCESS1 l43)

(AIRPORTACCESS2 l40)
(AIRPORTACCESS2 l50)
(AIRPORTACCESS2 l60)

(AIRPORTACCESS3 l53)
(AIRPORTACCESS3 l63)
(AIRPORTACCESS3 l70)
(OBJ p0)
(in t0 l01)
(in t1 l11)
(in t2 l22)
(in t3 l31)
(in t4 l42)
(in t5 l50)
(in t6 l60)
(in t7 l70)
(in p0 l02)
(in a0 l10)
(in a1 l33)
(in a2 l60)
(in a3 l63)
)
(:goal
(and
(in p0 l73)
)
)
)


