(define (problem roverprob4213) (:domain Rover)
(:objects
    general - Lander
    colour highres lowres - Mode
    rover0 - Rover
    rover0store - Store
    waypoint0 waypoint1 waypoint2 waypoint3 - Waypoint
    camera0 camera1 - Camera
    objective0 objective1 - Objective
	)
(:init
(visible waypoint0 waypoint1)
(visible waypoint1 waypoint0)
(visible waypoint1 waypoint2)
(visible waypoint2 waypoint1)
(visible waypoint1 waypoint3)
(visible waypoint3 waypoint1)
(visible waypoint2 waypoint0)
(visible waypoint0 waypoint2)
(visible waypoint2 waypoint3)
(visible waypoint3 waypoint2)
(visible waypoint3 waypoint0)
(visible waypoint0 waypoint3)
(atsoilsample waypoint0)
(atrocksample waypoint0)
(atlander general waypoint1)
(channelfree general)
(at rover0 waypoint0)
(available rover0)
(storeof rover0store rover0)
(empty rover0store)
(equippedforsoilanalysis rover0)
(equippedforrockanalysis rover0)
(equippedforimaging rover0)
(cantraverse rover0 waypoint0 waypoint1)
(cantraverse rover0 waypoint1 waypoint0)
(cantraverse rover0 waypoint0 waypoint2)
(cantraverse rover0 waypoint2 waypoint0)
(cantraverse rover0 waypoint0 waypoint3)
(cantraverse rover0 waypoint3 waypoint0)
(onboard camera0 rover0)
(calibrationtarget camera0 objective0)
(supports camera0 colour)
(supports camera0 highres)
(supports camera0 lowres)
(onboard camera1 rover0)
(calibrationtarget camera1 objective1)
(supports camera1 highres)
(visiblefrom objective0 waypoint0)
(visiblefrom objective1 waypoint0)
(visiblefrom objective1 waypoint1)
(visiblefrom objective1 waypoint2)
)

(:goal (and
(communicatedsoildata waypoint0)
(communicatedrockdata waypoint0)
(communicatedimagedata objective1 lowres)
	)
)
)