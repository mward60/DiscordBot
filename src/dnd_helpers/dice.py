from dnd_helpers.types.enums import DiceReturnCode
import random

DEFAULT_DICE_NUM_SIDES = 0
DEFAULT_DICE_NUM_DICE = 0
DEFAULT_DICE_MODIFIER = 0

class Dice():
    """ Dungeons and Dragons Dice Class
    """
    def __init__(self) -> None:
        self._n_sides = DEFAULT_DICE_NUM_SIDES
        self._n_dice = DEFAULT_DICE_NUM_DICE
        self._modifier = DEFAULT_DICE_MODIFIER
        self._dice_str = None

    @property
    def roll_dice(self) -> str:
        """ Getter method for dice roll result. Rolls dice with given number of \
            sides, number of dice, and modifier, if any.
        """

        rolls = []

        for i in range(int(self._n_dice)):
            rolls.append(random.randint(1, int(self._n_sides)))
        total = sum(rolls)

        # Rolls should be sorted to look a little neater
        rolls.sort(reverse = True)
        
        if self._modifier == 0:
            return f"**Result: {total}** ({self._dice_str}) {rolls}"
        
        elif self._modifier > 0:
            return f"**Result: {total + self._modifier}** ({self._dice_str}) {rolls} (+{self._modifier})"
            
        else:
            return f"**Result: {total + self._modifier}** ({self._dice_str}) {rolls} ({self._modifier})"
         

    @property
    def dice_str(self) -> str:
        return self._dice_str

    @dice_str.setter
    def dice_str(self, dice_str):
        self._dice_str = dice_str

    @property
    def n_sides(self) -> int:
        """ Getter function for 

        Returns:
            int: _description_
        """
        return self._n_sides
    
    @n_sides.setter
    def n_sides(self, sides):
        self._n_sides = sides

    @property
    def n_dice(self):
        return self._n_dice
    
    @n_dice.setter
    def n_dice(self, dice):
        self._n_dice = dice

    @property
    def modifier(self) -> int:
        return self._modifier
    
    @modifier.setter
    def modifier(self, modifier) -> None:
        self._modifier = modifier

def dice_string_parse(dice_str: str, dice: Dice) -> DiceReturnCode:
    """ Parses dice string and populates dice. Returns 0 if dice \
        string is valid. Returns -1 if string is invalid.

    Args:
        dice_str (str): Dice string to be parsed
        dice (Dice): Dice object to be populated

    Returns:
        int: Return code 
    """
    
    dice_str.replace(" ","")
    number_of_dice, number_of_sides_and_modifier = dice_str.split("d")

    
    
    # Checking for whether or not a modifier exists
    if number_of_sides_and_modifier.isnumeric():
        dice.modifier = 0
        dice.n_sides = number_of_sides_and_modifier

    else:
        if "+" in number_of_sides_and_modifier:
            sides, modifier = number_of_sides_and_modifier.split("+")
            dice.modifier = int(modifier)
            dice.n_sides = sides

        elif "-" in number_of_sides_and_modifier:
            sides, modifier = number_of_sides_and_modifier.split("-")
            dice.modifier = int(modifier) * -1
            dice.n_sides = sides

        else:
            return DiceReturnCode.DICE_RETURN_CODE_FAILURE
    
    dice.n_dice = number_of_dice
    dice.dice_str = dice_str
    
    return DiceReturnCode.DICE_RETURN_CODE_SUCCESS