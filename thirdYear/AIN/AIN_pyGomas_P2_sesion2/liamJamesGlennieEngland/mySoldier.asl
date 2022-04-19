//TEAM_ALLIED

+flag (F): team(100)
  <-
  .get_service("captain").

//Cuando el agente coge la bandera, avisa al capitán de que lo tiene
+flag_taken: team(100) & not returning
  <-
  .print("In ASL, TEAM_ALLIED flag_taken");
  ?base(B);
  +returning;
  .goto(B);
  .get_service("captain");
  .wait(2000);
  ?captain(Captain);
  ?position(Pos);
  .send(Captain, tell, flagTaken(Pos)).


//Avisar al capitán de que ha llegado a su posición en la formación
+target_reached(T): team(100) & goingToFormation(Captain)
  <- 
  -goingToFormation(_);
  .send(Captain, tell, readyToGo).

//Ha llegado a la posición establecida del paquete 
+target_reached(T): team(100) & goneForPack
  <- 
  -goneForPack;
  .turn(0.375);
  if(flagTaken) {
    ?base(B);
    .goto(B);
    +returning;
  } else {
    ?flag(F);
    .goto(F);
  }.

//Si ve a un enemigo, compurueba que no puede haber fuego amigo y dispara
+enemies_in_fov(_, _, _, _, _, Position)
  <-
  .look_at(Position);
  +canShoot;
  if(friends_in_fov(_,_,_,_,_,AlliedPos)) {
    if (canShoot) {
      ?position(MyPos);
      .friendlyFire(MyPos, Position, AlliedPos, Res);
      if (Res) {
        -canShoot;
      }
    }
  }

  if (canShoot) {
    .shoot(5, Position);
  }
  
  -canShoot.

//Pedir salud si tiene menos de 95
+health(H): H<95 & not askingForHealth
  <-
  +askingForHealth.

//Pedir munición si tiene menos de 50
+ammo(A): A<50 & not askingForAmmo
  <-
  +askingForAmmo.

//Comunicarle al capitán que necesita salud, no podrá volver a pedir hasta dentro de 10 segundos
+askingForHealth
  <-
  .get_service("captain");
  .wait(500);
  ?captain(C);
  ?position(MyPos);
  .send(C, tell, askForHealth(MyPos));
  .wait(10000);
  -askingForHealth.

//Comunicarle al capitán que necesita munición, no podrá volver a pedir hasta dentro de 10 segundos
+askingForAmmo
  <-
  .get_service("captain");
  .wait(500);
  ?captain(C);
  ?position(MyPos);
  .send(C, tell, askForAmmo(MyPos));
  .wait(10000);
  -askingForAmmo.


//Ir a la posición recibida del capitán
+headTo(Pos)[source(Captain)]
  <-
  .goto(Pos);
  -headTo(Pos);
  if(askingForHealth | askingForAmmo) {
    +goneForPack;
  }.

//Ir a su posición en la formación
+formation(Pos)[source(Captain)]
  <-
  .goto(Pos);
  +goingToFormation(Captain);
  -formation(_).

//Si alguien ha cogido la bandera, vuelve a la base
+flagTaken[source(Captain)]: not goneForPack
  <-
  ?base(B);
  .goto(B);
  +returning.

//Solo ir a por un paquete si lo ha pedido
+packs_in_fov(ID,Type,Angle,Distance,Health,Position): Type < 1003 & goneForPack & not goneForClosePack
  <-
  -goneForPack;
  //Get the health pack
  if (Type == 1001 & askingForHealth) {
    .look_at(Position);
    .goto(Position);
    +goneForClosePack;
  }

  //Get the ammo pack
  if (Type == 1002 & askingForAmmo) {
    .look_at(Position);
    .goto(Position);
    +goneForClosePack;
  }.


//Quitar la creencia adecuada dependiendo del paquete recogido
+pack_taken(Type, N)
  <-
  -goneForClosePack;
  if(Type == "Medic"){
    -askingForHealth;
  } else {
    -askingForAmmo;
  }.