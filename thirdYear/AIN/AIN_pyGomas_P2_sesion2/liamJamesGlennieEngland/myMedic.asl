//TEAM_ALLIED

+flag (F): team(100)
  <-
  .get_service("captain").

//Cuando el agente coge la bandera, avisa al capitán de que lo tiene
+flag_taken: team(100) & not (returning | helping(_, _))
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

//Ha llegado a la posición acordada para curar al soldado
+target_reached(T): team(100) & helping(_, _)
  <- 
  -helping(_, _);
  .cure;
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

//Curarse si la salud está por debajo de 50
+health(H): H<50 & not selfCure
  <-
  .cure;
  +selfCure.

//Pedir munición si tiene menos de 50
+ammo(A): A<50 & not askingForAmmo
  <-
  +askingForAmmo.

//Acepta la petición de salud por parte del capitán
+askForHealth(Pos)[source(Captain)]: not (helping(_,_))
  <-
  ?position(MyPos);
  .send(Captain, tell, medicFree(MyPos));
  +helping(Captain, Pos);
  -askForHealth(_).

//Rechaza la petición de salud por parte del capitán
+askForHealth(_)[source(Captain)]: helping(_,_)
  <-
  .send(Captain, tell, medicBusy).

//Ir a la posición recibida del capitán
+headTo(Pos)[source(Captain)]
  <-
  .goto(Pos);
  -headTo(Pos);
  if(askingForAmmo) {
    +goneForPack;
  }.

//Ir a su posición en la formación
+formation(Pos)[source(Captain)]
  <-
  .goto(Pos);
  +goingToFormation(Captain);
  -formation(_).

//Si alguien ha cogido la bandera, vuelve a la base
+flagTaken[source(Captain)]: not helping(_, _)
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
    -selfCure;
  } else {
    -askingForAmmo;
  }.