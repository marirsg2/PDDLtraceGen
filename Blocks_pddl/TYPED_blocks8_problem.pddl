(define (problem BLOCKS-4-0)
(:domain BLOCKS)
(:objects
    A B C D E F G H - tblock)
(:INIT
(CLEAR C)
(CLEAR A)
(CLEAR B)
(CLEAR D)
(CLEAR E)
(CLEAR F)
(CLEAR G)
(CLEAR H)
(ONTABLE C)
(ONTABLE A)
(ONTABLE B)
(ONTABLE D)
(ONTABLE E)
(ONTABLE F)
(ONTABLE G)
(ONTABLE H)
(HANDEMPTY))
(:goal
(AND
(on D C )
(on C B )
(on B A )
)
)
)