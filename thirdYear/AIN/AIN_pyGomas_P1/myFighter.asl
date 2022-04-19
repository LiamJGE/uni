//EJEMPLO LUCHADOR 

+flag(F): team(200)
  <-
  +control_points([[70, 0, 70], [70, 0, 184], [184, 0, 184], [184, 0, 70]]);
  +total_control_points(4);
  +patrolling;
  +patroll_point(0);
  +rotateLikeaMF;
  +checkPos.
  // .print("Got control points:", C).

//Reached patroll point
+target_reached(T): patrolling & not shooting
 <-
  ?patroll_point(P);
  -patroll_point(P);
  +patroll_point(P+1);
  -target_reached(T).
  // .print("He llegado al punto: ", T).

+target_reached(T): shooting
 <-
  -stopRotating;
  +patrolling;
  +patroll_point(3);
  -target_reached(T);
  -shooting.

//Go to next patroll point
+patroll_point(P): total_control_points(T) & P<T
  <-
  ?control_points(C);
  .nth(P,C,A);
  // .print("Going to: ", A);
  .goto(A).

//Reached last patroll point
+patroll_point(P): total_control_points(T) & P==T
  <-
  -patroll_point(P);
  +patroll_point(0).



+packs_in_fov(ID,Type,Angle,Distance,Health,Position): Type < 1003 & not aporpaquete
  <-

  //Get the health pack
  ?health(H);
  if (Type == 1001 & H <= 50) {
    // .print("El paquete en fov es de vida");
    .look_at(Position);
    -stopRotating;
    .goto(Position);
    +aporpaquete;
  }

  //Get the ammo pack
  ?ammo(A); 
  if (Type == 1002 & A <= 50) {
    // .print("El paquete en fov es de ammo");
    .look_at(Position);
    -stopRotating;
    .goto(Position);
    +aporpaquete;
  }.


+friends_in_fov(ID,Type,Angle,Distance,Health,Position) : not needHealth
  <-
  ?ammo(MyAmmo);
  if(MyAmmo > 0) {
    // .print("Disparando");
    +stopRotating;
    .shoot(100,Position);
    // .stop;
    // -patroll_point(P);
    // -patrolling;
    // .goto(Position);
    +shooting;
  }.

+friends_in_fov(ID,Type,Angle,Distance,Health,Position) : needHealth
  <-
  ?health(MyHealth);
  if(MyHealth < Health) {
    -patroll_point(P);
    -patrolling;
    ?position([X,Y,Z]);
    .goto([-(X-255), Y, Z]);
  }.  


+pack_taken(Type, N)
<-
  // .print("Pack taken", Type, N);
  -aporpaquete;
  +patrolling;
  +patroll_point(3).

//Need a health pack
+health(H): H<30 & not aporpaquete
  <-
  // .print("I need a health pack");
  -patroll_point(P);
  -patrolling;
  .goto([118, 0, 118]);
  +needHealth.

+health(H): not shooting
  <-
  .wait(500);
  ?health(NewH);
  ?ammo(A);
  //Being attacked
  if(H > NewH & A > 0) {
    -patrolling;
    -patroll_point(P);
    .stop;
  }.

//Need ammo
+ammo(X): X=0 & not aporpaquete
  <-
  // .print("I need ammo");
  -patroll_point(P);
  -patrolling;
  .goto([118, 0, 118]);
  +needAmmo.

+ammo(X): X<10 & not aporpaquete & not shooting
  <-
  // .print("I need ammo");
  -patroll_point(P);
  -patrolling;
  .goto([118, 0, 118]);
  +needAmmo.

//Check if still shooting
+ammo(X): shooting
<-
  .wait(1500);
  ?ammo(NewX);
  if(X = NewX) {
    ?position(Pos);
    +target_reached(Pos);
  }
  
  -ammo(X);
  +ammo(NewX).

//Rotate to look for 
// +rotateLikeaMF: not stopRotating & not shooting
//   <-
//   // .print("Rotating like a motherfucker!");
//   .turn(1.57);
//   .wait(500);
//   -rotateLikeaMF;
//   +rotateLikeaMF.

+needHealth
  <-
  .print("I need health").

+needAmmo
  <-
  .print("I need ammo").

// +checkPos: not aporpaquete & not shooting
//   <-
//   ?position([X, Y, Z]);
//   .wait(3000);
//   ?position([NewX, NewY, NewZ]);

//   if (not patrolling) {
//     +patrolling;
//     +patroll_point(1);
//   }

//   if(NewX = X & NewZ = Z) {
//     ?patroll_point(P);
//     -patroll_point(P);
//     +patroll_point(P+1);
//   }

//   -checkPos;
//   +checkPos.


//Methods to be done
//1. Flee from a fight if health or ammo is low
//2. Fix when being shot to look for enemy
//3. If stuck, move with pos(MyPos)
//4. If enemy seen, chase them if health and ammo allow