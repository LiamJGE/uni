;; =========================================================
;; ===      B R E A D T H     A N D      D E P T H      ====
;; =========================================================

(defglobal ?*nod-gen* = 0)

;; Liam del futuro, no te olvides de comprobar la profundidad(level)

(defrule right
  ?f1 <-(robotPosition ?x ?y boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level ?lvl movement ?mov)
  ?f2 <- (buildingSize ?xLimit ?yLimit)
  ?f3 <- (holes $?holePositions)
  ?f4 <- (ladders $?ladderPositions)
  (max-depth ?prof)

  (test (neq ?mov left))
  (test (<= (+ ?lvl 1) ?prof))
  (test (<= (+ ?x 1) ?xLimit))
  (test (not (member$ (create$ hole (+ ?x 1) ?y) $?holePositions)))
  (test (not (member$ (create$ e (+ ?x 1) ?y) $?enemiesXY)))
  ;;(test (not (member$ (create$ b (+ ?x 1) ?y) $?boxesPositions)))
  =>
  (assert (robotPosition (+ ?x 1) ?y boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level (+ ?lvl 1) movement right))
  (bind ?*nod-gen* (+ ?*nod-gen* 1)))

(defrule left
  ?f1 <-(robotPosition ?x ?y boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level ?lvl movement ?mov)
  ?f2 <- (buildingSize ?xLimit ?yLimit)
  ?f3 <- (holes $?holePositions)
  ?f4 <- (ladders $?ladderPositions)
  (max-depth ?prof)

  (test (neq ?mov right))
  (test (<= (+ ?lvl 1) ?prof))
  (test (> (- ?x 1) 0))
  (test (not (member$ (create$ hole (- ?x 1) ?y) $?holePositions)))
  (test (not (member$ (create$ e (- ?x 1) ?y) $?enemiesXY)))
  ;;(test (not (member$ (create$ b (- ?x 1) ?y) $?boxesPositions)))
  =>
  (assert (robotPosition (- ?x 1) ?y boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level (+ ?lvl 1) movement left))
  (bind ?*nod-gen* (+ ?*nod-gen* 1)))

(defrule up
  ?f1 <-(robotPosition ?x ?y boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level ?lvl movement ?mov)
  ?f2 <- (buildingSize ?xLimit ?yLimit)
  ?f3 <- (ladders $?ladderPositions)
  (max-depth ?prof)
  
  (test (neq ?mov down))
  (test (<= (+ ?lvl 1) ?prof))
  (test (<= (+ ?y 1) ?yLimit))
  (test (member$ (create$ ladder ?x ?y) $?ladderPositions))
  ;;(test (not (member$ (create$ e ?x (+ ?y 1)) $?enemiesXY)))
  ;;(test (not (member$ (create$ b ?x (+ ?y 1)) $?boxesPositions)))
  =>
  (assert (robotPosition ?x (+ ?y 1) boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level (+ ?lvl 1) movement up))
  (bind ?*nod-gen* (+ ?*nod-gen* 1)))

(defrule down
  ?f1 <-(robotPosition ?x ?y boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level ?lvl movement ?mov)
  ?f2 <- (buildingSize ?xLimit ?yLimit)
  ?f3 <- (ladders $?ladderPositions)
  (max-depth ?prof)
  
  (test (neq ?mov up))
  (test (<= (+ ?lvl 1) ?prof))
  (test (> (- ?y 1) 0))
  (test (member$ (create$ ladder ?x (- ?y 1)) $?ladderPositions))
  =>
  (assert (robotPosition ?x (- ?y 1) boxes $?boxesPositions enemies $?enemiesXY bullets ?bulletNum level (+ ?lvl 1) movement down))
  (bind ?*nod-gen* (+ ?*nod-gen* 1)))

(defrule pickUpBox
  ?f1 <-(robotPosition ?x ?y boxes $?boxesPositionsLeft b ?x ?y $?boxesPositionsRight enemies $?enemiesXY bullets ?bulletNum level ?lvl movement ?mov)
  (max-depth ?prof)
  (test (<= (+ ?lvl 1) ?prof))
  =>
  (assert (robotPosition ?x ?y boxes $?boxesPositionsLeft $?boxesPositionsRight enemies $?enemiesXY bullets ?bulletNum level (+ ?lvl 1) movement pickUpBox))
  (bind ?*nod-gen* (+ ?*nod-gen* 1)))

(defrule shoot
  ?f1 <-(robotPosition ?x ?y boxes $?boxesPositions enemies $?enemiesPositionsRight e ?enemyX ?y $?enemiesPositionsLeft bullets ?bulletNum level ?lvl movement ?mov)
  (max-depth ?prof)
  (test (<= (+ ?lvl 1) ?prof))
  (test (> ?bulletNum 0))
  (test (or (= ?enemyX (+ ?x 1)) (= ?enemyX (- ?x 1))))
  =>
  (assert (robotPosition ?x ?y boxes $?boxesPositions enemies $?enemiesPositionsRight $?enemiesPositionsLeft bullets (- ?bulletNum 1) level (+ ?lvl 1) movement shoot))
  (bind ?*nod-gen* (+ ?*nod-gen* 1)))

;; ========================================================
;; =========      S E A R C H   S T R A T E G Y    ========
;; ========================================================
;; The goal rule is used to detect when the goal state has been reached 

(defrule goal
    (declare (salience 100))
    ;;?f<-(robotPosition ? ? boxes enemies $? bullets ?)
      ?f <- (robotPosition ? ? boxes enemies $? bullets ? level ? movement ?)
    
   =>
    ;;(printout t "SOLUTION FOUND AT LEVEL " ?n crlf)
    (printout t "NUMBER OF EXPANDED NODES OR TRIGGERED RULES " ?*nod-gen* crlf)
    (printout t "GOAL FACT " ?f crlf)
    
    (halt))

(defrule no_solution
    (declare (salience -99))
    ?f <- (robotPosition ? ? boxes enemies $? bullets ? level ? movement ?)

    
=>
    (printout t "SOLUTION NOT FOUND" crlf)
    (printout t "NUMBER OF EXPANDED NODES OR TRIGGERED RULES " ?*nod-gen* crlf)
    
    (halt))		


(deffunction start ()
    (reset)
	(printout t "Maximum depth:= " )
	(bind ?prof (read))
	
    (printout t "Search strategy " crlf "    1.- Breadth" crlf "    2.- Depth" crlf )
	(bind ?a (read))
	
    (if (= ?a 1)
        then    (set-strategy breadth)
        else   (set-strategy depth))
    
    (printout t " Execute run to start the program " crlf)
	
    ;;(assert (puzzle 2 8 3 1 6 4 7 0 5 level 0 movement null fact 0))
	  ;;(deffacts (puzzle 8 1 3 7 2 5 4 0 6 level 0 movement null fact 0))
    (assert (robotPosition 1 1 boxes b 11 2 b 4 3 b 3 4 enemies e 1 2 e 4 2 e 8 2 e 8 4 bullets 2 level 0 movement null)
        (ladders ladder 3 1 ladder 7 1 ladder 2 2 ladder 10 2 ladder 1 3  ladder 7 3 ladder 11 3 )
        (holes hole 5 2 hole 3 3 hole 8 3 hole 4 4 hole 5 4 hole 6 4)
        (buildingSize 11 4)
    )

	(assert (max-depth ?prof))
	
)