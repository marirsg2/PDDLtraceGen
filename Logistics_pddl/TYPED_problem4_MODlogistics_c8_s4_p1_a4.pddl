


(define (problem logistics-c8-s4-p1-a4)
(:domain logistics-strips)
(:objects
          c0 c1 c2 c3 c4 c5 c6 c7 - tCITY
          a0 a1 a2 a3 a4 a5 a6 - tAIRPLANE
          l00 l10 l20 l30 l40 l50 l60 l70 l01 l02 l03 l11 l12 l13 l21 l22 l23 l31 l32 l33 l41 l42 l43 l51 l52 l53 l61 l62 l63 l71 l72 l73 - tLOCATION
          p0 - tOBJ
          t0 t1 t2 t3 t4 t5 t6 t7 - tTRUCK

)
; The major modification is that the airplanes are both regular airplanes (for loading and unloading) as well as special airplanes for accessing specific
; subset of cities. This separates the cities.
; a0 a1 a2 a3 - tAIRPLANE
;IMPORTANT in-city is swapped to inCity. "-" is used as a special character and allowed in naming. This is a mistake for a language specification.
; IMPORTANT do NOT use "_" in any naming

(:init
(OBJ p0)
(CITY c0)
(CITY c1)
(CITY c2)
(CITY c3)
(CITY c4)
(CITY c5)
(CITY c6)
(CITY c7)
(AIRPLANE a0)
(AIRPLANE a1)
(AIRPLANE a2)
(AIRPLANE a3)
(AIRPLANE a4)
(AIRPLANE a5)
(AIRPLANE a6)

(AIRPORT l00)
(AIRPORT l01)

(AIRPORT l10)
(AIRPORT l11)

(AIRPORT l20)
(AIRPORT l23)

(AIRPORT l30)
(AIRPORT l33)

(AIRPORT l40)
(AIRPORT l41)
(AIRPORT l43)

(AIRPORT l50)
(AIRPORT l51)
(AIRPORT l53)

(AIRPORT l60)
(AIRPORT l61)
(AIRPORT l63)

(AIRPORT l70)
(AIRPORT l73)
(TRUCK t0)
(TRUCK t1)
(TRUCK t2)
(TRUCK t3)
(TRUCK t4)
(TRUCK t5)
(TRUCK t6)
(TRUCK t7)
(drivesInside t0 c0)
(drivesInside t1 c1)
(drivesInside t2 c2)
(drivesInside t3 c3)
(drivesInside t4 c4)
(drivesInside t5 c5)
(drivesInside t6 c6)
(drivesInside t7 c7)
(LOCATION l00)
(inCity l00 c0)
(LOCATION l01)
(inCity l01 c0)
(LOCATION l02)
(inCity l02 c0)
(LOCATION l03)
(inCity l03 c0)
(LOCATION l10)
(inCity l10 c1)
(LOCATION l11)
(inCity l11 c1)
(LOCATION l12)
(inCity l12 c1)
(LOCATION l13)
(inCity l13 c1)
(LOCATION l20)
(inCity l20 c2)
(LOCATION l21)
(inCity l21 c2)
(LOCATION l22)
(inCity l22 c2)
(LOCATION l23)
(inCity l23 c2)
(LOCATION l30)
(inCity l30 c3)
(LOCATION l31)
(inCity l31 c3)
(LOCATION l32)
(inCity l32 c3)
(LOCATION l33)
(inCity l33 c3)
(LOCATION l40)
(inCity l40 c4)
(LOCATION l41)
(inCity l41 c4)
(LOCATION l42)
(inCity l42 c4)
(LOCATION l43)
(inCity l43 c4)
(LOCATION l50)
(inCity l50 c5)
(LOCATION l51)
(inCity l51 c5)
(LOCATION l52)
(inCity l52 c5)
(LOCATION l53)
(inCity l53 c5)
(LOCATION l60)
(inCity l60 c6)
(LOCATION l61)
(inCity l61 c6)
(LOCATION l62)
(inCity l62 c6)
(LOCATION l63)
(inCity l63 c6)
(LOCATION l70)
(inCity l70 c7)
(LOCATION l71)
(inCity l71 c7)
(LOCATION l72)
(inCity l72 c7)
(LOCATION l73)
(inCity l73 c7)


(fliesTo a0 l00)
(fliesTo a0 l10)
(fliesTo a0 l20)
(fliesTo a0 l30)

(fliesTo a1 l33)
(fliesTo a1 l43)

(fliesTo a2 l40)
(fliesTo a2 l50)
(fliesTo a2 l60)

(fliesTo a3 l53)
(fliesTo a3 l63)
(fliesTo a3 l70)

(fliesTo a4 l23)
(fliesTo a4 l73)

(fliesTo a5 l11)
(fliesTo a5 l51)

(fliesTo a6 l01)
(fliesTo a6 l41)


(in t0 l00)
(in t1 l11)
(in t2 l22)
(in t3 l31)
(in t4 l42)
(in t5 l50)
(in t6 l60)
(in t7 l70)
(in a0 l00)
(in a1 l43)
(in a2 l60)
(in a3 l63)
(in a4 l23)
(in a5 l11)
(in a6 l41)
(in p0 l00)

)
(:goal

(and
(in p0 l73)
)

)
)


