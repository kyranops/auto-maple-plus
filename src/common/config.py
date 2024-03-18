"""A collection of variables shared across multiple modules."""


#########################
#       Constants       #
#########################
RESOURCES_DIR = 'resources'


#################################
#       Global Variables        #
#################################
# The player's position relative to the minimap
player_pos = (0, 0)

# Describes whether the main bot loop is currently running or not
enabled = False

# If there is another player in the map, Auto Maple will purposely make random human-like mistakes
stage_fright = False

# Represents the current shortest path that the bot is taking
path = []


#############################
#       Shared Modules      #
#############################
# A Routine object that manages the 'machine code' of the current routine
routine = None

# Stores the Layout object associated with the current routine
layout = None

# Shares the main bot loop
bot = None

# Shares the video capture loop
capture = None

# Shares the keyboard listener
listener = None

# Shares the gui to all modules
gui = None

# Shares the webhook to all modules
webhook = None


##############################
#       Watcher Flags        #
##############################
# Describes whether rune cool down in cooling down
rune_cd = False

# Cursed rune appeared
cursed_rune = False

# No damage numbers
no_damage_numbers = False

# Map overcrowded
map_overcrowded = False

# Violetta minigame
violetta_minigame = False

# Lie detector failed
lie_detector_failed = False

# Game disconnected
game_disconnected = False

# Character dead
character_dead = False

# Describes whether white (GM/Other user chat) detected in chat box
chatbox_msg = False

# Inside cashshop for extended period
stuck_in_cs = False

# Character in town
char_in_town = False

# Player not moving
player_stuck = False

# Polo portal
polo_portal = False

#Especia portal
especia_portal = False

#Player in town
in_town = False