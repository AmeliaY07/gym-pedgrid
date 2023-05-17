
from gym_minigrid.agents import BlueAdlerPedAgent
from gym_minigrid.agents import Lanes
import math

from gym_minigrid.wrappers import DirectionObsWrapper as Direction




def test_gap_facing_0():

    pedVMax = 4

    y = 1
    x = 30

    agent1 = BlueAdlerPedAgent(
        id=1,
        position=(x,y),
        direction=Direction.LR,
        speed=3,
        DML=False,
        p_exchg=0.0,
        pedVmax=pedVMax
    )

    agent2 = BlueAdlerPedAgent(
        id=2,
        position=(x + 1,1),
        direction=Direction.RL,
        speed=3,
        DML=False,
        p_exchg=0.0,
        pedVmax=pedVMax
    )

    agents = [agent1, agent2]

    sameAgents, oppAgents = agent1.getSameAndOppositeAgents(agents)

    gap_opposite, closestOpp = agent1.computeOppGapAndAgent(oppAgents)

    print(gap_opposite, closestOpp)

    assert oppAgents == [agent2]
    assert closestOpp == agent2

    assert gap_opposite == 0

def test_gap_facing_sameposition():

    pedVMax = 4

    y = 1
    x = 30

    agent1 = BlueAdlerPedAgent(
        id=1,
        position=(x,y),
        direction=Direction.LR,
        speed=3,
        DML=False,
        p_exchg=0.0,
        pedVmax=pedVMax
    )

    agent2 = BlueAdlerPedAgent(
        id=2,
        position=(x,y),
        direction=Direction.RL,
        speed=3,
        DML=False,
        p_exchg=0.0,
        pedVmax=pedVMax
    )

    agents = [agent1, agent2]

    sameAgents, oppAgents = agent1.getSameAndOppositeAgents(agents)

    gap_opposite, closestOpp = agent1.computeOppGapAndAgent(oppAgents)

    print(gap_opposite, closestOpp)

    assert oppAgents == [agent2]
    assert closestOpp == agent2

    assert gap_opposite == 0
    # assert agentOppIndex == -1



def test_gp_opp_0_to_10_LR():
    pedVMax = 3
    y = 1
    x = 3

    agent1 = BlueAdlerPedAgent(
        id=1,
        position=(x,y),
        direction=Direction.LR,
        speed=3,
        DML=False,
        p_exchg=0.0,
        pedVmax=pedVMax
    )

    for cellsBetween in range(10):
        agent2 = BlueAdlerPedAgent(
            id=2,
            position=(x+cellsBetween+1,y),
            direction=Direction.RL,
            speed=3,
            DML=False,
            p_exchg=0.0,
            pedVmax=pedVMax
        )

        agents = [agent1, agent2]

        sameAgents, oppAgents = agent1.getSameAndOppositeAgents(agents, laneOffset=0)
        gap_opposite, closestOpp = agent1.computeOppGapAndAgent(oppAgents)

        expectedGap = min(pedVMax,  math.ceil(cellsBetween / 2))
        assert oppAgents == [agent2]
        assert gap_opposite == expectedGap
        if math.ceil(cellsBetween / 2) <= pedVMax:
            assert closestOpp == agent2
        else:
            assert closestOpp is None


def test_gp_opp_0_to_10_RL():
    pedVMax = 4
    y = 1
    x = 30

    agent1 = BlueAdlerPedAgent(
        id=1,
        position=(x,y),
        direction=Direction.RL,
        speed=3,
        DML=False,
        p_exchg=0.0,
        pedVmax=pedVMax
    )

    for cellsBetween in range(10):
        agent2 = BlueAdlerPedAgent(
            id=2,
            position=(x - cellsBetween - 1,y),
            direction=Direction.LR,
            speed=3,
            DML=False,
            p_exchg=0.0,
            pedVmax=pedVMax
        )

        agents = [agent1, agent2]

        sameAgents, oppAgents = agent1.getSameAndOppositeAgents(agents, laneOffset=0)
        gap_opposite, closestOpp = agent1.computeOppGapAndAgent(oppAgents)

        expectedGap = min(pedVMax,  math.ceil(cellsBetween / 2))
        assert oppAgents == [agent2]
        assert gap_opposite == expectedGap
        if math.ceil(cellsBetween / 2) <= pedVMax:
            assert closestOpp == agent2
        else:
            assert closestOpp is None