from .PedestrianEnv import PedestrianEnv

from typing import List
from gym_minigrid.minigrid import *
from gym_minigrid.register import register
from gym_minigrid.agents import *
from gym_minigrid.envs.pedestrian.PedGrid import PedGrid
from gym_minigrid.lib.Action import Action
from gym_minigrid.lib.LaneAction import LaneAction
from gym_minigrid.lib.ForwardAction import ForwardAction
from gym_minigrid.lib.Direction import Direction
from gym_minigrid.lib.VehicleAction import VehicleAction
from .EnvEvent import EnvEvent
import logging
import random

class TwoLaneRoadEnv(PedestrianEnv):
    # Write the outline here how it should work

    # generic object representation
    # generic actors?
    def __init__(
        self,
        pedAgents: List[PedAgent]=[],
        vehicleAgents: List[Vehicle]=[],
        road: Road=None,
        sidewalks: List[Sidewalk]=[],
        crosswalks: List[Crosswalk]=[],
        width=8,
        height=8,
        stepsIgnore = 100
    ):
        
        self.vehicleAgents = vehicleAgents
        self.road = road
        self.sidewalks = sidewalks
        self.crosswalks = crosswalks
        
        super().__init__(
            pedAgents=pedAgents,
            width=width,
            height=height,
            stepsIgnore=stepsIgnore
        )

        self.updateActionHandlers({VehicleAction : self.executeVehicleAction})
        # TODO label each tile with either lane/sidewalk?

        pass

    def getVehicleAgents(self):
        return self.vehicleAgents
    
    def addVehicleAgents(self, agents: List[Vehicle]):
        for agent in agents:
            self.addVehicleAgent(agent)
    
    def addVehicleAgent(self, agent: Vehicle):
        self.vehicleAgents.append(agent)
        # subscribe to events here
        super().subscribe(EnvEvent.stepParallel2, agent.go)

    def getNumVehicleAgents(self):
        return len(self.vehicleAgents)
    
    def resetVehicleAgents(self):
        for agent in self.vehicleAgents:
            agent.reset()
    
    def reset(self):
        if self.vehicleAgents != None:
            self.resetVehicleAgents()
        super().reset()
    
    def removeVehicleAgent(self, agent: Vehicle):
        if agent in self.vehicleAgents:
            # unsubscribe to events here
            self.vehicleAgents.remove(agent)
            super().unsubscribe(EnvEvent.stepParallel2, agent.go)
        else:
            logging.warn("Agent not in list")
    
    def forwardVehicle(self, agent: Vehicle):
        assert agent.direction >= 0 and agent.direction < 4
        # fwd_pos = agent.topLeft + agent.speed * DIR_TO_VEC[agent.direction]
        # if fwd_pos[0] < 0 or fwd_pos[0] + agent.width >= self.width \
        #     or fwd_pos[1] < 0 or fwd_pos[1] + agent.height >= self.height:
        #     logging.warn("Vehicle cannot be moved here - out of bounds")
        newTopLeft = agent.topLeft + agent.speed * DIR_TO_VEC[agent.direction]
        newBottomRight = agent.bottomRight + agent.speed * DIR_TO_VEC[agent.direction]

        if newTopLeft[0] < 0 or newBottomRight[0] >= self.width \
            or newTopLeft[1] < 0 or newBottomRight[1] >= self.height:
            logging.warn("Vehicle cannot be moved here - out of bounds")
            agent.direction = (agent.direction + 2) % 4
        else:
            agent.topLeft = newTopLeft
            agent.bottomRight = newBottomRight
        # Get the contents of the cell in front of the agent
        # fwd_cell = self.grid.get(*fwd_pos)

        # # Move forward if no overlap
        # if fwd_cell == None or fwd_cell.can_overlap():
        
        # ^ can be problematic because moving objects may overlap with
        # other objects' previous positions
            # agent.topLeft = fwd_pos
            # agent.bottomRight = (fwd_pos[0]+agent.width, fwd_pos[1]+agent.height)

    def executeVehicleAction(self, action: Action):
        if action is None:
            return 

        agent = action.agent

        logging.debug(f"forwarding vehicle {agent.id}")

        self.forwardVehicle(agent)

    def render(self, mode='human', close=False, highlight=True, tile_size=TILE_PIXELS):
        """
        Render the whole-grid human view
        """

        if close:
            if self.window:
                self.window.close()
            return

        if mode == 'human' and not self.window:
            import gym_minigrid.window
            self.window = gym_minigrid.window.Window('gym_minigrid')
            self.window.show(block=False)

        # self._gen_grid(self.width, self.height)
        # ^ if we want the walls and old "goal" sidewalks

        img = self.grid.render(
            tile_size=tile_size,
            pedAgents=self.pedAgents,
            vehicleAgents=self.vehicleAgents,
            roads=[self.road],
            sidewalks=self.sidewalks,
            crosswalks=self.crosswalks,
            agent_pos=self.agent_pos,
            agent_dir=self.agent_dir,
            highlight_mask=None
            # highlight_mask=highlight_mask if highlight else None
        )

        if mode == 'human':
            self.window.set_caption(self.mission)
            self.window.show_img(img)

        return img

class TwoLaneRoadEnv60x80(TwoLaneRoadEnv):
    def __init__(self):
        width = 60
        height = 80

        lane1 = Lane(
            topLeft=(10, 0),
            bottomRight=(24, 79),
            direction=1,
            inRoad=1,
            laneID=1,
            posRelativeToCenter=1
        )
        lane2 = Lane(
            topLeft=(35, 0),
            bottomRight=(49, 79),
            direction=3,
            inRoad=1,
            laneID=2,
            posRelativeToCenter=-1
        )
        road1 = Road([lane1, lane2], roadID=1)

        sidewalk1 = Sidewalk(
            topLeft=(0, 0),
            bottomRight=(9, 79),
            sidewalkID=1
        )

        sidewalk2 = Sidewalk(
            topLeft=(25, 0),
            bottomRight=(34, 79),
            sidewalkID=2
        )

        sidewalk3 = Sidewalk(
            topLeft=(50, 0),
            bottomRight=(59, 79),
            sidewalkID=3
        )

        crosswalk1 = Crosswalk(
            topLeft=(10, 40),
            bottomRight=(24, 45),
            crosswalkID=1
        )

        crosswalk2 = Crosswalk(
            topLeft=(35, 40),
            bottomRight=(49, 45),
            crosswalkID=2
        )

        super().__init__(
            road=road1,
            sidewalks=[sidewalk1, sidewalk2, sidewalk3],
            crosswalks=[crosswalk1, crosswalk2],
            width=width,
            height=height
        )

register(
    id='TwoLaneRoadEnv60x80-v0',
    entry_point='gym_minigrid.envs.pedestrian.TwoLaneRoadEnv:TwoLaneRoadEnv60x80'
)

register(
    id='TwoLaneRoadEnv-20x80-v0',
    entry_point='gym_minigrid.envs.pedestrian.TwoLaneRoadEnv:TwoLaneRoadEnv'
)