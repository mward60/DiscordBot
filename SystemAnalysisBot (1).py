import discord, random
from discord import app_commands, Button
from typing import Literal, Optional

# This is what allows our code to interface with Discord
intents = discord.Intents.default()
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

# Unique bot token that can't be put online or else Discord forces a re-generation
TOKEN='MTIyNDQzMTU4ODcxMzAzNzgyNA.GJfs0-.Gv3YsfrsL1rwAWIIwUAweE9XBNOoVoxBfK_s7A'

@client.event
async def on_ready():
    # Sets the bot to be "playing dungeons and dragons"
    print("Setting bot activity...")
    activity = discord.Game(name="/roll", type=3)
    await client.change_presence(status = discord.Status.idle, activity=activity)
    print(f"Bot activity set to {activity}.")
    
    # Logs every guild that IvyBot is present in
    for guild in client.guilds:
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
        print(f'{client.user.name} is connected to {guild.name}.')
        print(f'Server Members ({len(guild.members)}):')
        for member in guild.members:
            print(f'- {member.name}')

# Changes the "playing dungeons and dragons"    
@tree.command(
    name="setactivity",
    description="Sets the bot's activity"
)
async def changeactivy(interaction, activity:str, status:Literal[1,2,3,4]):
    activity = discord.Game(name=activity, type=status)
    await client.change_presence(status = discord.Status.idle, activity=activity)
    await interaction.response.send_message(f"Bot activity set to {activity}.")
    
# Takes input and splits it into readable dice commands
@tree.command(
    name="roll",
    description="Rolls a number of dice in xdy+z format.",
)
async def first_command(interaction, dice:str):
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

@tree.command(
     name="dndstats",
     description="Rolls ability scores for D&D 5e using the 4d6 drop lowest method.",
)
async def fortysix(interaction):
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

@tree.command(
    name='fireball',
    description='fireball wins again'
)
async def fireroll(interaction, level:int):
    if level < 3:
        await interaction.response.send_message(f'Fireball is a 3rd-level spell. Try again.')
    if level > 9:
        await interaction.response.send_message(f"You can't cast spells higher than 9th-level. Try again.")
    rolls = []
    for i in range (0,5+level):
        rolls.append(random.randint(1,6))
    total = sum(rolls)
    await interaction.response.send_message(f'**Result: {total} fire damage!** `{level+5}d6 = {rolls}`' + ' https://tenor.com/view/xptolevel3-xptolvl3-jacob-budz-jacob-budz-gif-27231246')

@tree.command(
    name='dndidea',
    description='Generates a random race and class for your next 5e character.',
)
async def cherry(interaction):
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

    #Check if a subrace is even present, for races like half-orc and tiefling
    if charsubrace == '':
        await interaction.response.send_message(f'You should play a {charrace} {charclass} with the {charbackground} background!')
    else:
        await interaction.response.send_message(f'You should play a {charsubrace} {charrace} {charclass} with the {charbackground} background!')    

# Sadly this command was overshadowed by Discord itself in a recent update
@tree.command(
    name='vote',
    description='Separate up to six phrases with commas to create a call for a vote.'
)
async def makepoll(interaction, items:str):
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

@tree.command(
    name='dndcharacter',
    description="Generates an entire D&D character complete with ability scores, class, race, and background."
)
async def newcharacter(interaction):
    # Stitches together everything from previous interactions in order to make an entire character
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

@tree.command(
    name='dndracials',
    description="Displays the racial traits of any race available in the D&D 5e Player's Handbook."
)
async def newcharacter(interaction, race: Literal['Dwarf, Hill','Dwarf, Mountain','Elf, High','Elf, Wood','Drow','Halfling, Lightfoot','Halfling, Stout','Human','Dragonborn','Gnome, Forest','Gnome, Rock','Half-Elf','Half-Orc','Tiefling']):
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

@tree.command(
    name='dndmonster',
    description="Displays a random monster from the D&D 5e Monster Manual."
)
async def newmonster(interaction):
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
@tree.command(
    name="sroll",
    description="Rolls a skill check for Fallout: Seattle. Roll-at-or-under is a success!"
)
async def seattleroll(interaction, skill:Literal["Barter", "Big Guns", "Energy Weapons",
                    "Explosives","Lockpick","Medicine","Melee Weapons", "Repair",
                    "Science","Small Guns","Sneak","Speech","Unarmed"],
                      value:int, penalties:int):
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

@tree.command(
    name="schargen",
    description="Generates a new character for Fallout: Seattle."
)
async def seattlechargen(interaction, race:Literal["RANDOM","Human - Vault Dweller","Human - Wastelander","Ghoul","Synth - Unaware","Synth - Aware",
                                                   "Robot - Mister Handy","Robot - Assaultron","Robot - Protectron"]):
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

client.run(TOKEN)