
import random

def _get_random_dice_rolls(dice_rolls_list: list[int]) -> None:
    """Populates dice rolls list with random values from 1 to 6

    Args:
        dice_rolls_list (list[int]): List of dice rolls
    """
    for i in range(0, 4):
        dice_rolls_list[i] = random.randint(1,6)
    dice_rolls_list.sort(reverse=True)

def _get_attribute_from_dice_rolls(dice_rolls: list[int]) -> int:
    """Calculates the attribute from list of randomly generated dice rolls

    Args:
        dice_rolls (list[int]): List of dice rolls

    Returns:
        int: Calculated attribute
    """
    minValue = min(dice_rolls)
    return (sum(dice_rolls) - minValue)

def get_attributes() -> str:
    """Returns the ability score. Rolls using 4d6 rules.

    Returns:
        str: Ability score string
    """
    attributes = [0, 0, 0, 0, 0, 0]
    dice_rolls = [0, 0, 0, 0]

    results = ""

    for i in range(0,6):
        _get_random_dice_rolls(dice_rolls)
        attributes[i] = _get_attribute_from_dice_rolls(dice_rolls)
        results += f'`{dice_rolls}` Result: `{attributes[i]}`\n'
    attributes.sort(reverse=True)

    return f'**Ability Scores: {attributes}**\n{results}'