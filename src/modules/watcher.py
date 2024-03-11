"""A module for detecting and notifying the user of dangerous in-game events."""

from src.common import config, utils
import time
from datetime import datetime
import os
import cv2
import pygame
import threading
import numpy as np
import keyboard as kb
from src.routine.components import Point
from src.common import config
from resources import watcher_scan_table
import pyautogui

# A rune's symbol on the minimap
RUNE_RANGES = (
    ((141, 148, 245), (146, 158, 255)),
)
rune_filtered = utils.filter_color(cv2.imread('assets/rune_template.png'), RUNE_RANGES)
RUNE_TEMPLATE = cv2.cvtColor(rune_filtered, cv2.COLOR_BGR2GRAY)

# Other players' symbols on the minimap
OTHER_RANGES = (
    ((0, 245, 215), (10, 255, 255)),
)
other_filtered = utils.filter_color(cv2.imread('assets/other_template.png'), OTHER_RANGES)
OTHER_TEMPLATE = cv2.cvtColor(other_filtered, cv2.COLOR_BGR2GRAY)

# The Elite Boss's warning sign
ELITE_TEMPLATE = cv2.imread('assets/elite_template.jpg', 0)

# Rune CD Templates
RUNE_CD1_TEMPLATE = cv2.imread('assets/runeCD.png', 0)
RUNE_CD2_TEMPLATE = cv2.imread('assets/runeCD2.png', 0)

# EXP Text as Chat Anchor
CHAT_ANCHOR = cv2.imread('assets/exp.png',0)


def get_alert_path(name):
    return os.path.join(Watcher.ALERTS_DIR, f'{name}.mp3')


class Watcher:
    ALERTS_DIR = os.path.join('assets', 'alerts')

    def __init__(self):
        self.ready = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

        self.room_change_threshold = 0.9
        self.rune_alert_delay = 270         # 4.5 minutes

        self.detectionTable = {}

    def start(self):
        """Starts this Watcher's thread."""
        print('\n[~] Started watcher')
        self.thread.start()

    def _main(self):
        self.ready = True
        rune_start_time = time.time()
        std = watcher_scan_table.scan_table_dynamic
        detectionTable = {}
        for scanEntry in std:
            detectionTable[scanEntry] = ""
        sts = watcher_scan_table.scan_table_static
        charLocation_Last = None

        while True:
            if config.enabled:
                frame = config.capture.frame #entire screen
                height, width, _ = frame.shape
                minimap = config.capture.minimap['minimap'] #minimap only
                
                # Check for rune CD
                runeCD1 = utils.multi_match(frame, RUNE_CD1_TEMPLATE, threshold=0.85)
                runeCD2 = utils.multi_match(frame, RUNE_CD2_TEMPLATE, threshold=0.85)
                if len(runeCD1) > 0 or len(runeCD2) > 0:
                    config.rune_cd = True
                else:
                    config.rune_cd = False

                # Check for rune
                now = time.time()
                if not config.bot.rune_active:
                    filtered = utils.filter_color(minimap, RUNE_RANGES)
                    matches = utils.multi_match(filtered, RUNE_TEMPLATE, threshold=0.9)
                    rune_start_time = now
                    if matches and config.routine.sequence:
                        abs_rune_pos = (matches[0][0], matches[0][1])
                        config.bot.rune_pos = utils.convert_to_relative(abs_rune_pos, minimap)
                        distances = list(map(distance_to_rune, config.routine.sequence))
                        index = np.argmin(distances)
                        config.bot.rune_closest_pos = config.routine[index].location
                        if config.rune_cd == False:
                            config.bot.rune_active = True
                elif now - rune_start_time > self.rune_alert_delay:     # Alert if rune hasn't been solved
                    config.bot.rune_active = False

                # Update key stats into monitoring console
                if config.rune_cd:
                    config.gui.view.monitoringconsole.set_runecdstat("Cooling down...")
                elif not config.rune_cd:
                    config.gui.view.monitoringconsole.set_runecdstat("Ready to Solve")

                # Check for number of other players in map
                filtered = utils.filter_color(minimap, OTHER_RANGES)
                others = len(utils.multi_match(filtered, OTHER_TEMPLATE, threshold=0.5))
                if others > 1:
                    config.map_overcrowded = True
                elif others <= 1:
                    config.map_overcrowded = False
                config.gui.view.monitoringconsole.set_noOthers(str(others))

                # Scan against dynamic scan table
                for scanEntry in std:
                    params = std[scanEntry]
                    flagname = params.get("flag")
                    target = cv2.imread("assets/"+params.get("ImgName"),0)
                    matchCount = utils.multi_match(frame=frame, template=target, threshold=0.8)                   
                    if params.get("Invert") == "False":
                        if matchCount != []:
                            if detectionTable[scanEntry] == "":
                                detectionTable[scanEntry] = datetime.now()
                            else:
                                firstDetection = detectionTable[scanEntry]
                                if (datetime.now() - firstDetection).total_seconds() > int(params.get("Threshold")):
                                    setattr(config,flagname,True)

                        else:
                            detectionTable[scanEntry] = ""
                            setattr(config,flagname,False)
                    if params.get("Invert") == "True":
                        if matchCount == []:
                            if detectionTable[scanEntry] == "":
                                detectionTable[scanEntry] = datetime.now()
                            else:
                                firstDetection = detectionTable[scanEntry]
                                if (datetime.now() - firstDetection).total_seconds() > int(params.get("Threshold")):
                                    setattr(config,flagname,True)
                        else:
                            detectionTable[scanEntry] = ""
                            setattr(config,flagname,False)

                #scan for chat
                CA_TopLeft, CA_TopRight = utils.single_match(frame=frame,template=CHAT_ANCHOR)
                if CA_TopLeft != None:

                    #step to screenshot, high chance to fail due to pyautogui bug?
                    pyautogui.screenshot("assets/chat.png",region=(CA_TopLeft[0]+5,CA_TopLeft[1]-60,390,50))
                    img = cv2.imread("assets/chat.png")

                    #remove specifically achievements mega
                    noAchiv = cv2.bitwise_and(img,img,mask=cv2.bitwise_not(cv2.inRange(img, (255,255,220), (255,255,230))))

                    # set white range and threshold
                    lowcolor =(210,210,210) #gm chat color is dimmest at 210 210 210
                    highcolor = (255,255,255) #pure white
                    thresh = cv2.inRange(noAchiv, lowcolor, highcolor)
                    #count pixels ch. is 19 pixels
                    count = np.count_nonzero(thresh)
                    if count >= 80:
                        config.chatbox_msg = True
                    else:
                        config.chatbox_msg = False
                else:
                    pass

                #scan for stationary
                if charLocation_Last == None:
                    charLocation_Last = config.player_pos
                    charLocation_Time = datetime.now()
                if charLocation_Last != config.player_pos:
                    charLocation_Last = config.player_pos
                    charLocation_Time = datetime.now()
                    setattr(config,"player_stuck",False)
                if config.player_pos == charLocation_Last and (datetime.now()-charLocation_Time).total_seconds() > 15:
                    setattr(config,"player_stuck",True)

                config.gui.runtime_console.runtimeFlags.update_All_Flags()
            time.sleep(0.05)


    def _alert(self, name, volume=0.75):
        """
        Plays an alert to notify user of a dangerous event. Stops the alert
        once the key bound to 'Start/stop' is pressed.
        """

        config.enabled = False
        config.listener.enabled = False
        self.mixer.load(get_alert_path(name))
        self.mixer.set_volume(volume)
        self.mixer.play(-1)
        while not kb.is_pressed(config.listener.config['Start/stop']):
            time.sleep(0.1)
        self.mixer.stop()
        time.sleep(2)
        config.listener.enabled = True

    def _ping(self, name, volume=0.5):
        """A quick notification for non-dangerous events."""

        self.mixer.load(get_alert_path(name))
        self.mixer.set_volume(volume)
        self.mixer.play()


#################################
#       Helper Functions        #
#################################
def distance_to_rune(point):
    """
    Calculates the distance from POINT to the rune.
    :param point:   The position to check.
    :return:        The distance from POINT to the rune, infinity if it is not a Point object.
    """

    if isinstance(point, Point):
        return utils.distance(config.bot.rune_pos, point.location)
    return float('inf')
