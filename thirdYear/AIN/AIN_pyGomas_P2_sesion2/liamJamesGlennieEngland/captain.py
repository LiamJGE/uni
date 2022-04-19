import json
import math
import random
import sys
from loguru import logger
from spade.behaviour import OneShotBehaviour
from spade.template import Template
from spade.message import Message
from pygomas.bditroop import BDITroop
from pygomas.bdifieldop import BDIFieldOp
from pygomas.bdisoldier import BDISoldier
from pygomas.bdimedic import BDIMedic
from agentspeak import Actions
from agentspeak import grounded
from agentspeak.stdlib import actions as asp_action
from pygomas.ontology import DESTINATION

from pygomas.agent import LONG_RECEIVE_WAIT


class BDICaptain(BDITroop):

    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        # Si el área del triángulo formado por 3 puntos (la posición del enemigo, aliado y la mía) 
        # es 0 y el aliado está en medio, habrá fuego amigo 
        @actions.add_function(".friendlyFire", (tuple, tuple, tuple))
        def _friendlyFire(myPos, enemyPos, alliedPos):
            areaTriangle = abs(round(myPos[0])*(enemyPos[2]-alliedPos[2]) + enemyPos[0]*(alliedPos[2]-round(myPos[2])) + alliedPos[0]*(round(myPos[2])-enemyPos[2]))
            if(areaTriangle < 1 and 
               ((myPos[0]<alliedPos[0]<enemyPos[0] and myPos[2]<alliedPos[2]<enemyPos[2]) 
               or (myPos[0]>alliedPos[0]>enemyPos[0] and myPos[2]>alliedPos[2]>enemyPos[2]))):
                return True
            else: return False


        
        # Calcula un punto cercano donde el médico o fieldop puede ayudar al soldado
        @actions.add_function(".findNearishPoint", (tuple, tuple))
        def _findNearishPoint(helperPos, soldierPos):
            return tuple((helperPos[0], 0, soldierPos[2]))

        # Crea los puntos para que se pueda formar un rombo alrededor del capitán y el médico
        @actions.add_function(".getFormationPoints", (tuple, tuple))
        def _getFormationPoints(basePos, flagPos):
            goDown = basePos[2] > flagPos[2]
            goLeft = basePos[0] > flagPos[0]

            multiplier = -1 if goDown else 1

            frontLine  = basePos[2] + multiplier * 30
            centerLine = basePos[2] + multiplier * 20
            backLine   = basePos[2] + multiplier * 10

            multiplier = -1 if goLeft else 1

            frontBackLeft   = basePos[0] + multiplier * 30
            frontBackMiddle = basePos[0] + multiplier * 20
            frontBackRight  = basePos[0] + multiplier * 10

            centerLeft     = basePos[0] + multiplier * 35
            centerMidLeft  = basePos[0] + multiplier * 25
            centerMidRight = basePos[0] + multiplier * 15
            centerRight    = basePos[0] + multiplier * 5

            positions = [tuple([frontBackLeft, 0,frontLine]), tuple([frontBackMiddle, 0,frontLine]), tuple([frontBackRight, 0,frontLine]),
                         tuple([centerLeft, 0, centerLine]), tuple([centerMidLeft, 0, centerLine]), tuple([centerMidRight, 0, centerLine]), tuple([centerRight, 0, centerLine]),
                         tuple([frontBackLeft, 0, backLine]), tuple([frontBackMiddle, 0, backLine]), tuple([frontBackRight, 0, backLine])]

            return tuple(positions)

        # Elimina el elemento la posición indicado en la lista pasado como parámetro
        @actions.add_function(".delete", (int, tuple))
        def _delete(pos, list):
            if pos == 0:
                return list[1:]
            elif pos == (len(list) - 1):
                return list[:pos]
            else:
                return tuple(list[0:pos] + list[pos + 1:])



class BDIMySoldier(BDISoldier):
    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        # Si el área del triángulo formado por 3 puntos (la posición del enemigo, aliado y la mía) 
        # es 0 y el aliado está en medio, habrá fuego amigo 
        @actions.add_function(".friendlyFire", (tuple, tuple, tuple))
        def _friendlyFire(myPos, enemyPos, alliedPos):
            areaTriangle = abs(round(myPos[0])*(enemyPos[2]-alliedPos[2]) + enemyPos[0]*(alliedPos[2]-round(myPos[2])) + alliedPos[0]*(round(myPos[2])-enemyPos[2]))
            if(areaTriangle < 1 and 
               ((myPos[0]<alliedPos[0]<enemyPos[0] and myPos[2]<alliedPos[2]<enemyPos[2]) 
               or (myPos[0]>alliedPos[0]>enemyPos[0] and myPos[2]>alliedPos[2]>enemyPos[2]))):
                return True
            else: return False

class BDIMyFieldOp(BDIFieldOp):
    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        # Si el área del triángulo formado por 3 puntos (la posición del enemigo, aliado y la mía) 
        # es 0 y el aliado está en medio, habrá fuego amigo 
        @actions.add_function(".friendlyFire", (tuple, tuple, tuple))
        def _friendlyFire(myPos, enemyPos, alliedPos):
            areaTriangle = abs(round(myPos[0])*(enemyPos[2]-alliedPos[2]) + enemyPos[0]*(alliedPos[2]-round(myPos[2])) + alliedPos[0]*(round(myPos[2])-enemyPos[2]))
            if(areaTriangle < 1 and 
               ((myPos[0]<alliedPos[0]<enemyPos[0] and myPos[2]<alliedPos[2]<enemyPos[2]) 
               or (myPos[0]>alliedPos[0]>enemyPos[0] and myPos[2]>alliedPos[2]>enemyPos[2]))):
                return True
            else: return False

class BDIMyMedic(BDIMedic):
    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        # Si el área del triángulo formado por 3 puntos (la posición del enemigo, aliado y la mía) 
        # es 0 y el aliado está en medio, habrá fuego amigo 
        @actions.add_function(".friendlyFire", (tuple, tuple, tuple))
        def _friendlyFire(myPos, enemyPos, alliedPos):
            areaTriangle = abs(round(myPos[0])*(enemyPos[2]-alliedPos[2]) + enemyPos[0]*(alliedPos[2]-round(myPos[2])) + alliedPos[0]*(round(myPos[2])-enemyPos[2]))
            if(areaTriangle < 1 and 
               ((myPos[0]<alliedPos[0]<enemyPos[0] and myPos[2]<alliedPos[2]<enemyPos[2]) 
               or (myPos[0]>alliedPos[0]>enemyPos[0] and myPos[2]>alliedPos[2]>enemyPos[2]))):
                return True
            else: return False