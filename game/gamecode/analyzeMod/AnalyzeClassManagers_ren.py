from renpy.store import Player, Monster, NoClassManager, classGenerators   # type: ignore
from renpy import narrator
"""renpy
init 1 python:
"""
from typing import Literal, Union

class AnalyzeClassManager(NoClassManager):

    
    MONSTERS: list[str] = []
    """
    List of Monsters that have been previously scanned by the player, and will automatically have their analyze informaiton available
    """
    CL_NAME = "Analyze"


class AnalyzeOwnerClassManager(AnalyzeClassManager):
    CL_TYPE = "Owner"

class AnalyzeTargetClassManager(AnalyzeClassManager):
    CL_TYPE = "Target"

    def __init__(self, char = None):
        super().__init__(char)

        if char and type(char) is Monster and char.IDname in self.MONSTERS:
            char.encyclopedia = "_Analyze"
    
    def analyzeEndChange(self, currTtip: str, char: 'Monster') -> str:
        self.MONSTERS.append(char.IDname)
        return super().analyzeEndChange(currTtip, char)

classGenerators["Analyze"]= { 
    "Owner": AnalyzeOwnerClassManager,
    "Target": AnalyzeTargetClassManager
}

        