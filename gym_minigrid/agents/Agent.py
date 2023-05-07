from typing import Tuple
from gym_minigrid.lib import BaseObject
import random
import numpy as np

class Agent(BaseObject):
    def __init__(
        self, 
        id,
        initTopLeft: Tuple[int, int],
        initBottomRight: Tuple[int, int],
        direction: int, # TODO convert direction to enum
        maxSpeed: float = 4,
        speed: float = 3,
        DML: bool = False, # TODO this is not a property of the agent.
        p_exchg: float = 0.0
        ):

        self.id = id

        self.DML = DML
        self.p_exchg = p_exchg

        super().__init__(
            initTopLeft=initTopLeft,
            initBottomRight=initBottomRight
        )

        self.initDirection = direction

        self.direction = direction
        self.maxSpeed = maxSpeed
        self.speed = speed

        self.canShiftLeft = True
        self.canShiftRight = True
        self.agentAction = 0 # Put this in PedAgent later, save agentActions here for execution
        # Agents will save the actions we compute
        # Once we execute, we get action from here
        
        self.gapSame = 8 # TODO transfer all the blue and alder properties
        self.gapOpp = 4
        
        pass

    def reset(self):
        # TODO 
        super().reset()
        self.direction = self.initDirection
        pass