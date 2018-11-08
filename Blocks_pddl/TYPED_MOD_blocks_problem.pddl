(define (problem BLOCKS-4-0)
(:domain BLOCKS)
(:objects
    D B A C -tblock
     H1 - thand
     T1 - ttable )
(:INIT
(under C none)
(under D none)
(under B none)
(under A none)
(onblock C noblock)
(onblock A noblock)
(onblock B noblock)
(onblock D noblock)
(holding H1 none)
(ontable A T1)
(ontable B T1)
(ontable C T1)
(ontable D T1)

)
(:goal
(AND
(ON D C)
(ON C B)
(ON B A)
)
)
)