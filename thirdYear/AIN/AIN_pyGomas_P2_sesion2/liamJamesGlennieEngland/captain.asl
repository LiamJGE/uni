//TEAM_ALLIED

//Registrar servicio, crear y comunicar los puntos de formación
+flag (F): team(100)
  <-
  .register_service("captain");
  ?base(B);
  .getFormationPoints(B, F, FormationPoints);
  +giveFormationOrder(FormationPoints).

//Si coge la bandera, avisa al resto de agentes para volver a la base
+flag_taken: team(100)
  <-
  .print("In ASL, TEAM_ALLIED flag_taken");
  .get_medics;
  .get_backups;
  .get_fieldops;
  .wait(2000);
  ?myMedics(M);
  ?myBackups(S);
  ?myFieldops(F);
  .send(M, tell, flagTaken);
  .send(S, tell, flagTaken);
  .send(F, tell, flagTaken);
  ?base(B);
  .goto(B).

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

// Recibe solictud de salud y le pide ayuda al médico
+askForHealth(Pos)[source(Soldier)]: not askingForHealth 
	<-
  +woundedSoldier(Soldier, Pos);
	+askingForHealth;
  .get_medics;
  .wait(500);
  if(myMedics(M)) {
    .send(M, tell, askForHealth(Pos));
    .wait(1000);
  }.

//El médico está disponible. Encuentra un punto cercano para los dos agentes
//y los manda a dicho punto
+medicFree(MedicPos)[source(Medic)]
  <-
  ?woundedSoldier(Soldier, SoldierPos);
  .findNearishPoint(MedicPos, SoldierPos, NearestPos);
  .wait(500);
  .send(Medic, tell, headTo(NearestPos));
  .send(Soldier, tell, headTo(NearestPos));
  -askingForHealth.

//El médico no está disponible, olvida la solicitud de ayuda porque 
//probablemente ya estará muerto el soldado
+medicBusy[source(Medic)]
  <-
  -askingForHelp.


// Recibe solictud de munición y le pide ayuda al fieldop
+askForAmmo(Pos)[source(Soldier)]: not askingForAmmo 
	<-
  +noAmmoSoldier(Soldier, Pos);
	+askingForAmmo;
  .get_fieldops;
  .wait(500);
  if(myFieldops(F)) {
    .send(F, tell, askForAmmo(Pos));
    .wait(1000);
  }.


//El fieldop está disponible. Encuentra un punto cercano para los dos agentes
//y los manda a dicho punto
+fieldopFree(FieldopPos)[source(Fieldop)]
  <-
  ?noAmmoSoldier(Soldier, SoldierPos);
  .findNearishPoint(FieldopPos, SoldierPos, NearestPos);
  .wait(500);
  .send(Fieldop, tell, headTo(NearestPos));
  .send(Soldier, tell, headTo(NearestPos));
  -askingForAmmo.

//El fieldop no está disponible, olvida la solicitud de ayuda porque 
//probablemente ya estará muerto el soldado
+fieldopBusy[source(Fieldop)]
  <-
  -askingForAmmo.

//Crea una lista de los agentes para comunicarles 
//las posiciones de la formación
+giveFormationOrder(FormationPoints)
  <-
  .get_medics;
  .get_backups;
  .get_fieldops;
  .wait(2000);
  ?myMedics(M);
  ?myBackups(S);
  ?myFieldops(F);
  +medics(M);
  +soldiers(S);
  +fieldops(F);
  +tellPositions(FormationPoints).

//Ordena a los agentes para que se pongan
//en su posición de la formación
+tellPositions(FormationPoints)
  <-
  .length(FormationPoints, L);
  if (L > 0){
    .nth(0, FormationPoints, Point);
    if (L == 6) {
      .goto(Point);
      .delete(0, FormationPoints, FPNew);
      -tellPositions(_);
      +tellPositions(FPNew);
    } 
    
    if(L == 5 & medics(M)) {
      .nth(0, M, Medic);
      -medics(_);
      .send(Medic, tell, formation(Point));
      .delete(0, FormationPoints, FPNew);
      -tellPositions(_);
      +tellPositions(FPNew);
    }
    
    if(L == 2 & fieldops(F)) {
      .nth(0, F, FieldOp);
      -fieldops(_);
      .send(FieldOp, tell, formation(Point));
      .delete(0, FormationPoints, FPNew);
      -tellPositions(_);
      +tellPositions(FPNew);
    } else {
      if (soldiers(S)){
        .nth(0, S, Soldier);
        .delete(0, S, S1);
        -soldiers(_);
        .length(S1, LS);
        if (LS > 0) {
          +soldiers(S1);
        }
        .send(Soldier, tell, formation(Point));
        .delete(0, FormationPoints, FPNew);
        -tellPositions(_);
        +tellPositions(FPNew);
      }  
    }
    
  } else {
    +readyMembers([]);
    -tellPositions(_);
  }.

//Los agentes le comunican que ya están en posición. Una vez estén todos 
//o hayan pasado 10 segundos desde que se recibió el último mensaje, 
//van todos a la bandera
+readyToGo[source(TroopMember)]: not rejectReadyToGoes
<-
  ?readyMembers(RM);
  .concat(RM, [TroopMember], RM1);
  -readyMembers(_);
  +readyMembers(RM1);
  .length(RM1, L);
  if(L == 9) {
    ?flag(F);
    .send(RM1, tell, headTo(F));
    .goto(F);
  } 
  else {
    .wait(10000);
    ?readyMembers(RM2);
    .length(RM2, L1);

    //Si hay agentes que se han quedado parados 
    //sin poder ir a su posición, abandonar la formación
    if(L == L1) {
      ?flag(F);  
      ?myMedics(M);
      ?myBackups(S);
      ?myFieldops(FO);
      .send(M, tell, headTo(F));
      .send(S, tell, headTo(F));
      .send(FO, tell, headTo(F));
      .goto(F);
      //No permite que los agentes parados hagan que todos vuelvan 
      //a la bandera cuando se lanza la siguiente creencia de target_reached
      +rejectReadyToGoes;
    }  
  }
  -readyToGo.

//Un agente ha cogido la bandera entonces el capitán
//manda al resto de agentes a la base
+flagTaken(Pos)[source(TroopMember)]
  <-
  .get_medics;
  .get_backups;
  .get_fieldops;
  .wait(2000);
  ?myMedics(M);
  ?myBackups(S);
  ?myFieldops(F);
  .send(M, tell, flagTaken);
  .send(S, tell, flagTaken);
  .send(F, tell, flagTaken);
  ?base(B);
  .goto(B).
// Wait until everyone in spot and then go for the flag --> DONE
// Asking for med and ammo packs 
// If someone has flag, let everyone know and they'll protect them hopefully
// Shooting tactics, asking for help if needed