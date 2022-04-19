+flag(F): team(200)
  <-
  +control_points([[70, 0, 70], [184, 0, 184], [70, 0, 184], [184, 0, 70]]);
  +total_control_points(4);
  +patrolling;
  +patroll_point(0);
  .print("Got control points:", C).


+target_reached(T): patrolling & team(200)
  <-
  ?patroll_point(P);
  -patroll_point(P);
  +patroll_point(P+1);
  .print("Target reached: ", T);
  -target_reached(T).

+target_reached(T): goneForPacks | inBattle | goneForClosePack | running
  <-
  -target_reached(T);
  -goneForPacks;
  -goneForClosePack;
  -running;
  +patrolling;
  +target_reached(T).


+patroll_point(P): total_control_points(T) & P<T
  <-
  ?control_points(C);
  .nth(P,C,A);
  .goto(A).

+patroll_point(P): total_control_points(T) & P==T
  <-
  -patroll_point(P);
  +patroll_point(0).
 

//A smart soldier would realize that it's low on health or ammo and go to the center and restock
+health(MyH): MyH<50 & not goneForPacks & not inBattle
  <-
  -patrolling;
  +goneForPacks;
  .stop;
  .goto([130, 0, 115]);
  .print("Gone for health pack").


+ammo(MyA): MyA<1 & not goneForPacks
  <-
  -patrolling;
  +goneForPacks;
  .stop;
  .goto([130, 0, 115]);
  .print("Gone for ammo pack").


+ammo(MyA): MyA<40 & not goneForPacks & not inBattle
  <-
  -patrolling;
  +goneForPacks;
  .stop;
  .goto([130, 0, 115]);
  .print("Gone for ammo pack").

//An even smarter soldier knows which pack it needs
+packs_in_fov(ID,Type,Angle,Distance,Health,Position): Type < 1003 & not goneForClosePack
  <-
  //Get the health pack
  ?health(H);
  if (Type == 1001 & H <= 50) {
    .look_at(Position);
    .goto(Position);
    +goneForClosePack;
  }

  //Get the ammo pack
  ?ammo(A); 
  if (Type == 1002 & A <= 50) {
    // .print("El paquete en fov es de ammo");
    .look_at(Position);
    .goto(Position);
    +goneForClosePack;
  }.

+ammo(A): inBattle
  <-
  .wait(1000);
  ?ammo(CurrentA);
  if(A=CurrentA & CurrentA < 40) {
    .stop;
    -inBattle;
    +ammo(CurrentA);
  }.


//We should detect when someone is shooting at us
+health(MyH): MyH<100 & not inBattle & not goneForClosePack
  <-
  .stop;
  .print("I'm being attacked");
  +rotateOnTheSpot;
  +healthCheck.

+rotateOnTheSpot: not inBattle
  <-
  .print("Rotating");
  .turn(1.57);
  .wait(3000);
  +rotateOnTheSpot.

//We check our health to see if we're are still under attack
+healthCheck
  <-
  ?health(H);
  .wait(500);
  ?health(CurrentHealth);
  .print("Health", H, CurrentHealth);
  //No longer in a battle
  if(H=CurrentHealth) {
    -rotateOnTheSpot;
    -healthCheck;
    -inBattle;
    .print("No longer in a battle");

    //Need a health/ammo pack
    ?ammo(A);
    if(CurrentHealth < 50 | A < 50) {
      -patrolling;
      +goneForPacks;
      .stop;
      .goto([130, 0, 115]);
    } else{
      .stop;
      ?patroll_point(P);
      -patroll_point(P);
      +patroll_point(P);
    }
  } else {
    +healthCheck;
  }.

    
//A megamind soldier would shoot anyone it sees, advise that it's in battle and stop rotating. Oh yeah and be agressive.
//However an even bigger brain soldier would evaluate the situation and calculate if it has a chance of surviving the battle
//If it doesn't, it runs. Simple as that
+friends_in_fov(ID,Type,Angle,Distance,Health,[X,Y,Z])
  <-
  ?health(MyH);
  ?ammo(MyA);

  if ((Health - MyH > 10 | Health - MyA > 30) & not inBattle) {
    .print("Running from enemy");
    ?position([MyX, MyY, MyZ]);

    //Now, elses didn't work here so don't blame me for this

    //If enemy up, go down
    if(MyX > X & X + Distance < 245) {
      -patrolling;
      +running;
      .stop;
      .goto([X + Distance, Y, Z]);
    }

    //If enemy down, go up
    if (MyX < X & X - Distance > 15) {
      -patrolling;
      +running;
      .stop;
      .goto([X - Distance, Y, Z]);
    }

    //If enemy left, go right
    if (MyZ > Z & X + Distance < 245) {
      -patrolling;
      +running;
      .stop;
      .goto([X, Y, Z + Distance]);
    }
    
    //If enemy right, go left
    if (MyZ < Z & Z - Distance > 15) {
          -patrolling;
          +running;
          .stop;
          .goto([X, Y, Z - Distance]);
    }
  }

  if(Health - MyH < 10 | Health - MyA < 30) {
    .shoot(5,[X, Y, Z]);
    if(not inBattle) {
      +inBattle;
      .print("I'm in a battle");
      -patrolling;
      .goto([X, Y, Z]);
    }
    -rotateOnTheSpot;
  }.
