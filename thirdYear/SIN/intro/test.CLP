  (deffacts people
    (person name John age 43)
    (person name Liam age 19)
    (person name Paul age 26)
    (person name Luke age 31))

  (defrule remove
    ?f1 <- (person name ?name age ?age)
           (test (< 30 ?age))	
        =>
           (retract ?f1)
           (assert (person name Joel age 25)))