#!/usr/bin/env python3

import discord, random
from discord import app_commands, Interaction, Intents, Client, Game, Status
from typing import Literal, Optional
from discord_token import *
from guild.guild import *

# This is what allows our code to interface with Discord
intents = Intents.default()
discord_client = Client(intents = Intents.all())
command_tree = app_commands.CommandTree(discord_client)

@discord_client.event
async def on_ready() -> None:
    """ Sets the bot to "Playing Dungeons and Dragons"
    """

    print("Setting bot activity...")

    dnd_discord_game = Game(name = "Dungeons and Dragons", type = 3)

    await discord_client.change_presence(activity = dnd_discord_game, status = Status.idle)
    print(f"Bot activity set to {dnd_discord_game}.")
    
    # Logs every guild that IvyBot is present in
    for guild in discord_client.guilds:
        command_tree.copy_global_to(guild = guild)
        await command_tree.sync(guild = guild)
    
    log_bot_guild_presence(discord_client)

# Changes the "playing dungeons and dragons"    
@command_tree.command(
    name="setactivitystatus",
    description="Sets the bot's activity"
)
async def bot_set_activity_status(interaction: Interaction, activity: str, status: discord.Status) -> None:
    """_summary_

    Args:
        interaction (Interaction): _description_
        activity (str): _description_
        status (discord.Status): 'online', 'offline', 'idle', 'dnd(do not disturb)', 'invisible'
    """
    #(cbwolfe94): Seems like status isn't needed in the constructor
    game = discord.Game(activity)

    await discord_client.change_presence(activity = game, status = status)
    await interaction.response.send_message(f"Bot activity set to {activity}.")
    
# Takes input and splits it into readable dice commands
@command_tree.command(
    name = "roll",
    description = "Rolls a number of dice in xdy+z format.",
)
async def bot_roll_dice(interaction: Interaction, dice: str) -> None:
    """ Discord bot will roll the number of dice in xdy + z format

    Args:
        interaction (_type_): Discord interaction
        dice (str): Dice string in xdy + z format
        #(cbwolfe94): I would put an example of a format for anyone who doesn't know the correct way to format the dice 
    """

    dice.replace(" ","")
    rolled = dice
    number, sides = dice.split("d")
    # Checking for whether or not a modifier exists
    if sides.isnumeric():
        modifier = 0

    else:
        if "+" in sides:
            sides, modifier = sides.split("+")
            modifier = int(modifier)
        elif "-" in sides:
            sides, modifier = sides.split("-")
            modifier = int(modifier) * -1
        else:
            await interaction.response.send_message(f"Please use xdy+z format for dice rolling with this command.")
    number = int(number)
    sides = int(sides)
    rolls = []
    for i in range(number):
        rolls.append(random.randint(1,sides))
    total = sum(rolls)
    # Rolls should be sorted to look a little neater
    rolls.sort(reverse=True)
    if modifier == 0:
        await interaction.response.send_message(f'**Result: {total}**  `{rolled} = {rolls}`')
    elif modifier > 0:
        await interaction.response.send_message(f'**Result: {total + modifier}**  `{rolled} = {rolls} (+{modifier})`')
    else:
        await interaction.response.send_message(f'**Result: {total + modifier}**  `{rolled} = {rolls} ({modifier})`')

@command_tree.command(
     name="dndstats",
     description="Rolls ability scores for D&D 5e using the 4d6 drop lowest method.",
)
async def bot_roll_ability_score_4d6(interaction: Interaction) -> None:
    """_summary_

    Args:
        interaction (_type_): _description_
    """
    results = ""
    attributes = [0,0,0,0,0,0]
    for i in range(0,6):
        dice = [0,0,0,0]
        for p in range(0,4):
            dice[p] = random.randint(1,6)
        dice.sort(reverse=True)
        # Stores a display value so that certain dice can be removed later
        results += f'`{dice}` Result: `{sum(dice) - min(dice)}`\n'
        dice.remove(min(dice))
        attributes[i] = sum(dice)
    attributes.sort(reverse=True)
    await interaction.response.send_message(f'**Ability Scores: {attributes}**\n{results}') 

@command_tree.command(
    name='fireball',
    description='fireball wins again'
)
async def bot_fireball_roll(interaction: Interaction, level: int) -> None:
    """_summary_

    Args:
        interaction (_type_): _description_
        level (int): _description_
    """
    if level < 3:
        await interaction.response.send_message(f'Fireball is a 3rd-level spell. Try again.')
    if level > 9:
        await interaction.response.send_message(f"You can't cast spells higher than 9th-level. Try again.")
    rolls = []
    for i in range (0,5+level):
        rolls.append(random.randint(1,6))
    total = sum(rolls)
    await interaction.response.send_message(f'**Result: {total} fire damage!** `{level+5}d6 = {rolls}`' + ' https://tenor.com/view/xptolevel3-xptolvl3-jacob-budz-jacob-budz-gif-27231246')

@command_tree.command(
    name='dndidea',
    description='Generates a random race and class for your next 5e character.',
)
async def cherry(interaction):
    """_summary_

    Args:
        interaction (_type_): _description_
    """

    #(cbwolfe94): I would change this function to a better name

    races = ['Dragonborn','Dwarf','Elf','Gnome','Half-Elf','Halfling','Half-Orc','Human','Tiefling']
    classes = ['Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard']
    backgrounds = ['Acolyte','Charlatan','Criminal','Entertainer','Folk Hero','Gladiator','Guild Artisan','Hermit','Knight','Noble','Outlander','Pirate','Sage','Sailor','Soldier','Spy','Urchin']
    charrace = races[random.randint(0,len(races) - 1)]
    charbackground = backgrounds[random.randint(0,len(backgrounds) - 1)]
    charclass = classes[random.randint(0,len(classes) - 1)]
    # Loops through for each race a list of subraces
    if charrace == 'Dragonborn':
        subraces = ['Black','Blue','Brass','Bronze','Copper','Gold','Green','Red','Silver','White']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Dwarf':
        subraces = ['Hill','Mountain','Duergar']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Elf':
        subraces = ['High','Wood','Drow','Sea']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Gnome':
        subraces = ['Rock','Forest','Deep']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Half-Elf':
        subraces = ['High','Wood','Drow']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Halfling':
        subraces = ['Lightfoot','Stout']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Half-Orc':
        subraces = ['']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Human':
        subraces = ['','Variant']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    else: # Tiefling
        subraces = ['']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]

    #Check if a subrace is present, for races like half-orc and tiefling
    if charsubrace == '':
        await interaction.response.send_message(f'You should play a {charrace} {charclass} with the {charbackground} background!')
    else:
        await interaction.response.send_message(f'You should play a {charsubrace} {charrace} {charclass} with the {charbackground} background!')    

# Sadly this command was overshadowed by Discord itself in a recent update
@command_tree.command(
    name='vote',
    description='Separate up to six phrases with commas to create a call for a vote.'
)
async def makepoll(interaction, items:str):
    """_summary_

    Args:
        interaction (_type_): _description_
        items (str): _description_
    """
    remainder = items
    choices = f'**{interaction.user} has called for a vote!**\n'
    commas = 0
    emojis = ['🔴','🟡','🔵','🟠','🟢','🟣']
    for character in items:
        if character == ',':
            # Essentially checks for number of commas to figure out which options should sit where
            if commas < 6:
                commas += 1
                item, remainder = remainder.split(',',1)
                choices += emojis[commas - 1] + ' ' + item.lstrip(' ') + '\n'
    if commas == 0:
        await interaction.response.send_message("You have to have more than one choice to take a vote on them!")
    else:
        choices += emojis[commas] + ' ' + remainder.lstrip(' ') + '\n'
        await interaction.response.send_message(choices)
        new_msg = await interaction.original_response()
        for i in range(0, commas + 1):
            # Reacts with each emoji so people can click them
            await new_msg.add_reaction(emojis[i])

@command_tree.command(
    name='dndcharacter',
    description="Generates an entire D&D character complete with ability scores, class, race, and background."
)
async def bot_make_new_character(interaction: Interaction) -> None:
    """ Stitches together everything from previous interactions in order to make an entire character

    Args:
        interaction (_type_): _description_
    """

    races = ['Dragonborn','Dwarf','Elf','Gnome','Half-Elf','Halfling','Half-Orc','Human','Tiefling']
    classes = ['Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin','Ranger','Rogue','Sorcerer','Warlock','Wizard']
    backgrounds = ['Acolyte','Charlatan','Criminal','Entertainer','Folk Hero','Gladiator','Guild Artisan','Hermit','Knight','Noble','Outlander','Pirate','Sage','Sailor','Soldier','Spy','Urchin']
    charrace = races[random.randint(0,len(races) - 1)]
    charbackground = backgrounds[random.randint(0,len(backgrounds) - 1)]
    charclass = classes[random.randint(0,len(classes) - 1)]
    if charrace == 'Dragonborn':
        subraces = ['Black','Blue','Brass','Bronze','Copper','Gold','Green','Red','Silver','White']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Dwarf':
        subraces = ['Hill','Mountain','Duergar']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Elf':
        subraces = ['High','Wood','Drow','Sea']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Gnome':
        subraces = ['Rock','Forest','Deep']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Half-Elf':
        subraces = ['High','Wood','Drow']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Halfling':
        subraces = ['Lightfoot','Stout']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Half-Orc':
        subraces = ['']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    elif charrace == 'Human':
        subraces = ['','Variant']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    else: # Tiefling
        subraces = ['']
        charsubrace = subraces[random.randint(0,len(subraces) - 1)]
    
    results = ""
    attributes = [0,0,0,0,0,0]
    for i in range(0,6):
        dice = [0,0,0,0]
        for p in range(0,4):
            dice[p] = random.randint(1,6)
        dice.sort(reverse=True)
        results += f'`{dice}` Result: `{sum(dice) - min(dice)}`\n'
        dice.remove(min(dice))
        attributes[i] = sum(dice)
    attributes.sort(reverse=True)
    
    if charsubrace == '':
        await interaction.response.send_message(f'**{charbackground} {charrace} {charclass}\nAbility Scores: {attributes}**\n{results}Remember to apply your racial attribute modifiers!')
    else:
        await interaction.response.send_message(f'**{charbackground} {charsubrace} {charrace} {charclass}\nAbility Scores: {attributes}**\n{results}Remember to apply your racial attribute modifiers!')

@command_tree.command(
    name='dndracials',
    description="Displays the racial traits of any race available in the D&D 5e Player's Handbook."
)
async def newcharacter(interaction, race: Literal['Dwarf, Hill','Dwarf, Mountain','Elf, High','Elf, Wood','Drow','Halfling, Lightfoot','Halfling, Stout','Human','Dragonborn','Gnome, Forest','Gnome, Rock','Half-Elf','Half-Orc','Tiefling']):
    """_summary_

    Args:
        interaction (Interaction): _description_
        race (Literal[str]: _description_
        # (cbwolfe94) You shouldn't have to define the list of strings literal in the function parameter. The type hint should just be Literal[str]. 
        # Honestly it could be just a string.
    """
    traitlist = ''
    racial_traits = {
        'Dwarf, Hill': ['Ability Score Increase: Constitution: +2, Wisdom: +1', 'Age: Up to 350 years.', 'Size: Medium', 'Speed: 25 feet', 'Darkvision', 'Dwarven Resilience', 'Dwarven Combat Training', "Tool Proficiency: Smith's tools, brewer's supplies, or mason's tools.", 'Stonecutting', 'Languages: Common, Dwarvish', 'Dwarven Toughness'],
        'Dwarf, Mountain': ['Ability Score Increase: Constitution +2, Strength +2', 'Age: Up to 350 years.', 'Size: Medium', 'Speed: 25 feet', 'Darkvision', 'Dwarven Resilience', 'Dwarven Combat Training', "Tool Proficiency: Smith's tools, brewer's supplies, or mason's tools.", 'Stonecutting', 'Languages: Common, Dwarvish', 'Dwarven Armor Training'],
        'Elf, High': ['Ability Score Increase: Dexterity +2, Intelligence +1', 'Age: Up to 750 years.', 'Size: Medium', 'Speed: 30 feet', 'Darkvision', 'Keen Senses', 'Fey Ancestry', 'Trance', 'Languages: Common, Elvish, one of choice', 'Elf Weapon Training', 'Cantrip'],
        'Elf, Wood': ['Ability Score Increase: Dexterity +2, Wisdom +1', 'Age: Up to 750 years.', 'Size: Medium', 'Speed: Fleet of Foot: 35 feet', 'Darkvision', 'Keen Senses', 'Fey Ancestry', 'Trance', 'Languages: Common, Elvish', 'Elf Weapon Training', 'Mask of the Wild'],
        'Drow': ['Ability Score Increase: Dexterity +2, Charisma +1', 'Age: Up to 750 years.', 'Size: Medium', 'Speed: 30 feet', 'Superior Darkvision', 'Keen Senses', 'Fey Ancestry', 'Trance', 'Languages: Common, Elvish', 'Sunlight Sensitivity', 'Drow Magic', 'Drow Weapon Training'],
        'Halfling, Lightfoot': ['Ability Score Increase: Dexterity +2, Charisma +1', 'Age: Up to a couple centuries.', 'Size: Small', 'Speed: 25 feet', 'Lucky', 'Brave', 'Halfling Nimbleness', 'Languages: Common, Halfling', 'Naturally Stealthy'],
        'Halfling, Stout': ['Ability Score Increase: Dexterity +2, Constitution +1', 'Age: Up to a couple centuries.', 'Size: Small', 'Speed: 25 feet', 'Lucky', 'Brave', 'Halfling Nimbleness', 'Languages: Common, Halfling', 'Stout Resilience'],
        'Human': ['Ability Score Increase: All abilities +1', 'Age: Up to less than a century.', 'Size: Medium', 'Speed: 30 feet', 'Languages: Common, one of choice'],
        'Dragonborn': ['Ability Score Increase: Strength +2, Charisma +1', 'Age: Up to 80.', 'Size: Medium', 'Speed: 30 feet', 'Draconic Ancestry', 'Breath Weapon', 'Damage Resistance', 'Languages: Common, Draconic'],
        'Gnome, Forest': ['Ability Score Increase: Intelligence +2, Dexterity +1', 'Age: Up to 350-500', 'Size: Small', 'Speed: 25 feet', 'Darkvision', 'Gnome Cunning', 'Languages: Common, Gnomish', 'Natural Illusionist', 'Speak with Small Beasts'],
        'Gnome, Rock': ['Ability Score Increase: Intelligence +2, Constitution +1', 'Age: Up to 350-500', 'Size: Small', 'Speed: 25 feet', 'Darkvision', 'Gnome Cunning', 'Languages: Common, Gnomish', "Artificer's Lore", 'Tinker'],
        'Half-Elf': ['Ability Score Increase: Charisma +2, two of choice +1', 'Age: Up to 180', 'Size: Medium', 'Speed: 30 feet', 'Darkvision', 'Fey Ancestry', 'Skill Versatility', 'Languages: Common, Elvish, one of choice'],
        'Half-Orc': ['Ability Score Increase: Strength +2, Constitution +1', 'Age: Up to 75', 'Size: Medium', 'Speed: 30 feet', 'Darkvision', 'Menacing', 'Relentless Endurance', 'Savage Attacks', 'Languages: Common, Orc'],
        'Tiefling': ['Ability Score Increase: Charisma +2, Intelligence +1', 'Age: Same as humans but with a few more years', 'Size: Medium', 'Speed: 30 feet', 'Darkvision', 'Hellish Resistance', 'Infernal Legacy', 'Languages: Common, Infernal']
    }
    # Simply pulls a list of traits and displays them in a digestible manner
    for trait in racial_traits[race]:
        traitlist += f'{trait}\n'     
    await interaction.response.send_message(f'Racial traits for {race}:\n{traitlist}')

@command_tree.command(
    name='dndmonster',
    description="Displays a random monster from the D&D 5e Monster Manual."
)
async def newmonster(interaction: Interaction) -> None:
    """_summary_

    Args:
        interaction (Interaction): _description_
    """

    monsters = [
        'Aarakocra',
        'Aboleth',
        'Angel',
        'Animated Object',
        'Ankheg',
        'Azer',
        'Banshee',
        'Basilisk',
        'Behir',
        'Beholder',
        'Blight',
        'Bugbear',
        'Bulette',
        'Bullywug',
        'Cambion',
        'Carrion Crawler',
        'Centaur',
        'Chimera',
        'Chuul',
        'Cloaker',
        'Cockatrice',
        'Couatl',
        'Crawling Claw',
        'Cyclops',
        'Darkmantle',
        'Death Knight',
        'Deep Gnome',
        'Demilich',
        'Demon',
        'Devil',
        'Dinosaur',
        'Displacer Beast',
        'Doppelganger',
        'Dracolich',
        'Dragon',
        'Dragon Turtle',
        'Drow',
        'Drider',
        'Dryad',
        'Duergar',
        'Elemental',
        'Empyrean',
        'Ettercap',
        'Ettin',
        'Faerie Dragon',
        'Flameskull',
        'Flumph',
        'Fomorian',
        'Fungi',
        'Galeb Duhr',
        'Gargoyle',
        'Genie',
        'Ghost',
        'Ghoul',
        'Giant',
        'Gibbering Mouthar',
        'Gith',
        'Gnoll',
        'Goblin',
        'Golem',
        'Gorgon',
        'Grell',
        'Grick',
        'Griffon',
        'Grimlock',
        'Hag',
        'Half-Dragon',
        'Harpy',
        'Hell Hound',
        'Helmed Horror',
        'Hippogriff',
        'Hobgoblin',
        'Homunculus',
        'Hook Horror',
        'Hydra',
        'Incubus',
        'Intellect Devourer',
        'Invisible Stalker',
        'Jackalwere',
        'Kenku',
        'Kobold',
        'Kraken',
        'Kuo-Toa',
        'Lamia',
        'Lich',
        'Lizardfolk',
        'Lycanthrope',
        'Magmin',
        'Manticore',
        'Medusa',
        'Mephit',
        'Merfolk',
        'Merrow',
        'Mimic',
        'Mind Flayer',
        'Minotaur',
        'Modrons',
        'Mummy',
        'Myconid',
        'Naga',
        'Nightmare',
        'Nothic',
        'Ogre',
        'Oni',
        'Ooze',
        'Orc',
        'Otyugh',
        'Owlbear',
        'Pegasus',
        'Peryton',
        'Piercer',
        'Pixie',
        'Psudodragon',
        'Purple Worm',
        'Quaggoth',
        'Rakshasa',
        'Remorhaze',
        'Revenant',
        'Roc',
        'Roper',
        'Rust Monster',
        'Sahuagin',
        'Salamander',
        'Satyr',
        'Scarecrow',
        'Shadow',
        'Shadow Dragon',
        'Shambling Mound',
        'Shield Guardian',
        'Skeleton',
        'Slaad',
        'Specter',
        'Sphinx',
        'Sprite',
        'Stirge',
        'Succubus',
        'Tarrasque',
        'Thri-Kreen',
        'Treant',
        'Troglodyte',
        'Troll',
        'Umber Hulk',
        'Unicorn',
        'Vampire',
        'Water Weird',
        'Wight',
        "Will-o'-Wisp",
        'Wraith',
        'Wyvern',
        'Xorn',
        'Yeti',
        'Yuan-Ti',
        'Yugoloth',
        'Zombie'
    ]

    # All this does is pulls from a big ol' list to show a random monster. Helpful for running a game
    pick = monsters[random.randint(0,len(monsters) - 1)]
    await interaction.response.send_message(f"A wild {pick} has appeared!")

# This is from a game I have been working on for some time
@command_tree.command(
    name="sroll",
    description="Rolls a skill check for Fallout: Seattle. Roll-at-or-under is a success!"
)
async def seattleroll(interaction, skill:Literal["Barter", "Big Guns", "Energy Weapons",
                    "Explosives","Lockpick","Medicine","Melee Weapons", "Repair",
                    "Science","Small Guns","Sneak","Speech","Unarmed"],
                      value:int, penalties:int):
    """_summary_

    Args:
        interaction (_type_): _description_
        skill (Literal[&quot;Barter&quot;, &quot;Big Guns&quot;, &quot;Energy Weapons&quot;, &quot;Explosives&quot;,&quot;Lockpick&quot;,&quot;Medicine&quot;,&quot;Melee Weapons&quot;, &quot;Repair&quot;, &quot;Science&quot;,&quot;Small Guns&quot;,&quot;Sneak&quot;,&quot;Speech&quot;,&quot;Unarmed&quot;]): _description_
        value (int): _description_
        penalties (int): _description_
    """

    roll = random.randint(1,20)
    # In the game each "penalty" is a -2 reduction to your roll, so this mods the total target in order to be compared to a roll
    value -= penalties * 2
    if roll == 20:
        await interaction.response.send_message(f"You rolled a **natural 20** and **critically failed** the {skill} {value} skill check.")
    else:
        if roll == 1:
            await interaction.response.send_message(f"You rolled a **natural 1** and **scored a crit** on the {skill} {value} skill check.")
        else:
            if roll <= value:
                await interaction.response.send_message(f"You rolled a **{roll}** and **succeeded** the {skill} {value} skill check.")
            else:
                await interaction.response.send_message(f"You rolled a **{roll}** and **failed** the {skill} {value} skill check.")

@command_tree.command(
    name="schargen",
    description="Generates a new character for Fallout: Seattle."
)
async def seattlechargen(interaction: Interaction, race: Literal["RANDOM","Human - Vault Dweller","Human - Wastelander","Ghoul","Synth - Unaware","Synth - Aware",
                                                   "Robot - Mister Handy","Robot - Assaultron","Robot - Protectron"]):
    """ 

    Args:
        interaction (_type_): _description_
        race (Literal[str]: _description_
    """
    origins = []
    special = [1,1,1,1,1,1,1]
    allocate = 25
    # I'm actually pretty proud of this one since it angles toward having some attributes higher and some lower based on remainder
    for i in range(1, len(special)-1):
        if allocate >= 10:
            special[i] = random.randint(1,10)
            allocate -= special[i] - 1
        else:
            special[i] = random.randint(1,allocate)
            allocate -= special[i] - 1
    # Equally proud of this one, as it doles out remaining attribute points based on what's there
    while allocate > 0:
        dole = random.randint(0,6)
        if special[dole] < 10:
            special[dole] += 1
            allocate -= 1        
    random.shuffle(special)
    
    # Allows a random race roll
    if race == "RANDOM":
        race = random.choice(["Human - Vault Dweller","Human - Wastelander","Ghoul","Synth - Unaware","Synth - Aware",
                       "Robot - Mister Handy","Robot - Assaultron","Robot - Protectron"])
    
    # Checks for compatible character origins based on highest attribute(s)
    highest = int(max(special))
    if highest == special[0]: # STRENGTH
        origins += ["Citizen","Farmer","Junkie"]
        if race == "Robot - Mister Handy" or race == "Robot - Assaultron" or race == "Robot - Protectron":
            origins -= ['Junkie']
        origin = random.choice(origins)
    if highest == special[1]: # PERCEPTION
        origins += ["Enclave Initiate","Institute Recruit"]
        origin = random.choice(origins)
    if highest == special[2]: # ENDURANCE
        origins += ["Brawler","Farmer","Junkie","Mechanic"]
        if race == "Robot - Mister Handy" or race == "Robot - Assaultron" or race == "Robot - Protectron":
            origins -= ['Junkie']
        origin = random.choice(origins)
    if highest == special[3]: # CHARISMA
        origins += ["Citizen","Trader"]
        origin = random.choice(origins)
    if highest == special[4]: # INTELLIGENCE
        origins += ["Doctor","Institute Recruit","Mechanic","Scientist"]
        origin = random.choice(origins)
    if highest == special[5]: # AGILITY
        origins += ["Brotherhood Squire","Courier","Explorer","Soldier"]
        origin = random.choice(origins)
    if highest == special[6]: # LUCK
        origins += ["Explorer","Vault Dweller"]
        origin = random.choice(origins)
        
    await interaction.response.send_message(f"**STR:** {special[0]}\n**PER:** {special[1]}\n**END:** {special[2]}\n**CHR:** {special[3]}\n**INT:** {special[4]}\n**AGI:** {special[5]}\n**LUK:** {special[6]}\n**Race:** {race}\n**Origin:** {origin}")

def main() -> int:
    """ Main entry point for discord bot application

    Returns:
        int: Returns 0 on successful execution of program
    """
    print("Connecting to IvyBot on discord client ... \r\n")
    discord_client.run(TOKEN)
    return 0

if __name__ == "__main__":
    main()