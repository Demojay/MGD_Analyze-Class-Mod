from renpy.store import Player, Monster, Perk, NoClassManager, classGenerators, modPerkTypes   # type: ignore
"""renpy
init 1 python:
"""
from typing import Union

class AnalyzeClassManager(NoClassManager):

    
    MONSTERS: list[str] = []
    """
    List of Monsters that have been previously scanned by the player, and will automatically have their analyze informaiton available
    """
    CL_NAME = "Analyze"

    global modPerkTypes
    modPerkTypes.append("NoAutoAnalyze")

    @staticmethod
    def resetViewedMonsters():
        AnalyzeClassManager.MONSTERS = []

class AnalyzeOwnerClassManager(AnalyzeClassManager):
    CL_TYPE = "Owner"

class AnalyzeTargetClassManager(AnalyzeClassManager):
    CL_TYPE = "Target"

    
    def _canBeAutoAnalysed(self, char: Monster) -> bool:
        """
        Internal function to see whether the given Monster has the "NoAutoAnalyze" perkType in their perks, meaning their status won't be automatically revealed
        :param char: Holder of this instance
        :type char: Monster
        :return True if the monster has no perk with the "NoAutoAnalyze" perkType
        :rtype bool
        """
        foundNoAutoAnalyze = False

        for perk in char.perks:
            if foundNoAutoAnalyze:
                break

            for perkType in perk.PerkType:
                if perkType == "NoAutoAnalyze":
                    foundNoAutoAnalyze = True
                    break
        
        return not foundNoAutoAnalyze

    def __init__(self, char = None):
        super().__init__(char)

        if char and type(char) is Monster and char.IDname in AnalyzeClassManager.MONSTERS:
            if self._canBeAutoAnalysed(char):
                char.encyclopedia = "_Analyze"
    
    def analyzeEndChange(self, currTtip: str, char: 'Monster') -> str:
        if char.IDname not in AnalyzeClassManager.MONSTERS:
            AnalyzeClassManager.MONSTERS.append(char.IDname)
        return super().analyzeEndChange(currTtip, char)
    
    def applyModPerkEffects(self, owner: Union['Player', 'Monster'], perk: 'Perk', toAdd: bool) -> None:

        """
        Makes the monster instance who has been given this perkType not analyzed. For use with monsters
        that spawn similar looking minions with them. Does not remove them from the internal viewed list. 
        """
        if type(owner) is Monster:
            for perkType in perk.PerkType:
                if perkType == "NoAutoAnalyze":
                    owner.encyclopedia = ""
                    break

classGenerators["Analyze"]= { 
    "Owner": AnalyzeOwnerClassManager,
    "Target": AnalyzeTargetClassManager
}

        