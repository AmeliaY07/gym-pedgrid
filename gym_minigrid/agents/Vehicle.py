from typing import Tuple, List
from gym_minigrid.agents.Agent import Agent
from gym_minigrid.lib.Action import Action
from gym_minigrid.lib.VehicleAction import VehicleAction

class Vehicle(Agent):
    def __init__(
        self,
        id,
        topLeft: Tuple[int, int],
        bottomRight: Tuple[int, int],
        direction: int,
        maxSpeed: float,
        speed: float,
        inRoad: int,
        inLane: int,
        objectType="Vehicle"
    ):
        super().__init__(
            id=id,
            topLeft=topLeft,
            bottomRight=bottomRight,
            direction=direction,
            maxSpeed=maxSpeed,
            speed=speed,
            objectType=objectType
        )
        
        self.inRoad = inRoad
        self.inLine = inLane
    
    def go(self, env):
        """
            Simply move forward
        """
        return Action(self, VehicleAction.KEEP)