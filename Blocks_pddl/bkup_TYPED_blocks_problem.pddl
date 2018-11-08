(define (problem BLOCKS-4-0)
(:domain BLOCKS)
(:objects
    D B A C - tblock )
(:INIT
(CLEAR C)
(CLEAR A)
(CLEAR B)
(CLEAR D)
(ONTABLE C)
(ONTABLE A)
(ONTABLE B)
(ONTABLE D)
(HANDEMPTY))
(:goal
(AND
(on D C )
(on C B )
(on B A )
)
)
)