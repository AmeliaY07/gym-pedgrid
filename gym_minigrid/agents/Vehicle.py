from typing import Tuple, List
from gym_minigrid.agents.BaseObject import BaseObject

class Vehicle:
    def __init__(
        self,
        topLeft: Tuple[int, int],
        bottomRight: Tuple[int, int]
    ):
        super.__init__(
            topLeft=topLeft,
            bottomRight=bottomRight
        )