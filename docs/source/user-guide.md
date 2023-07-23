# User Guide

## Making and Customizing Environments
1. Wrap the desired environment class
2. Super initialize with custom parameters (*only height and width are supported as of now)

```python
class PedestrianEnv20x80(PedestrianEnv):
    def ___init__(self):
        width = 80
        height = 20
        super().__init__(
            width=width,
            height=height,
            pedAgents=None
        )
```

3. Register the child class environment with gym-minigrid

```python
register(
    id='PedestrianEnv-20x80-v0',
    entry_point='gym_minigrid.envs.pedestrian.PedestrianEnv:PedestrianEnv20x80'
)
```

4. Make the environment with gym
env = gym.make('PedestrianEnv-20x80-v0')

In the future, parameters will be incorporated into gym's make function.

## How to Use the MetricCollector
The MetricCollector observes an environment for a defined number of time steps and can be declared as such:

metricCollector = MetricCollector(env, stepsToIgnoreAtTheBeginning = , stepsToRecord = )

Suppose stepsToIgnoreAtTheBeginning = 100 and stepsToRecord = 1000; then, the MetricCollector will observe and maintain the metrics for time steps 101 to 1100.

## How to Create & Add Simple Pedestrians, Vehicles, and Road Infrastructure to an Environment
Example Pedestrian:
```python
ped = PedAgent(id=1, position=(x, y), direction=Direction.North, maxSpeed=5, speed=5)
env.addPedAgent(ped)
```

Alternatively, a list of pedestrians can be appended at once:
```python
peds = [ped_1, ped_2, ped_n]
env.addPedAgents(peds)
```

Example Vehicle:
```python
veh = Vehicle(id: 1, topLeft=(x1, x2), bottomRight=(x2, y2), direction=Direction.East, maxSpeed=20, speed=20, inRoad=1, inLane=1)
env.addVehicleAgent(veh)
```

Similarly, a list of vehicles can be appended with:
```python
env.addVehicleAgents()
```

Example Lane:
```python
lane = Lane(
    topLeft=(x1, y1),
    bottomRight=(x2, y2),
    direction=Direction.South,
    inRoad=1,
    laneID=1,
    posRelativeToCenter=-1
)
```

Example Road:
```python
road = Road(lanes=[lane1, lane2], roadID=1)
```

Example Sidewalk:
```python
sidewalk = Sidewalk(
    topLeft=(x1, y1),
    bottomRight=(x2, y2),
    sidewalkID=1
)
```

Example Crosswalk:
```python
crosswalk1 = Crosswalk(
    topLeft=(x1, y1),
    bottomRight=(x2, y2),
    crosswalkID=1,
    overlapRoad=1,
    overlapLanes=[1, 2] # laneIDs of the lanes
)
```

## Rendering:
Suppose we want to run a simulation for 1,000 steps. Rendering each step would take considerable time. Thus, rendering can be turned off by commenting out env.render() or controlled to only render at interval steps via modulus. This way, the simulation will run much quicker.

## PedestrianEnv

### Description:
This environment models a simple grid for behavior simulation involving pedestrians, containing a G<sub>m x n</sub> grid with customizable length m and height n. PedestrianEnv only supports pedestrian agents, or PedAgents. No other static or dynamic objects are supported. Pedestrians may be added or removed any time during simulation.

### Action Space:
PedGrid utilizes **_Action_** objects with properties _agent_ with the agent reference and _action_ as an enum. Currently, there are two enum classes defining dynamic agent movement.
* LaneAction
    * .KEEP: agent keeps the current lane
    * .LEFT: agent shifts a tile to the left
    * .RIGHT: agent shifts a tile to the right
* ForwardAction
    * .KEEP: agent moves forward by agent.speed tiles

**Note:** When a pedestrian agent reaches the end of the environment during a forward action, they automatically turn around in the opposite direction.

![Action Space](action-space.png)