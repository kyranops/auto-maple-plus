from src.common.interfaces import Configurable
import threading
from discord import SyncWebhook, File
import time
from datetime import datetime
import pytz
from src.gui.notifier_settings.main import NotifSettings
from src.gui.notifier_settings.notification_settings import NotificationSetting
from src.gui.automation.main import AutomationParams
import src.common.config as config
import pyautogui
import cv2
from pathlib import Path
import src.modules.automation as automation

class Notifier:
    def __init__(self):
        self.ready = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True
        
    def start(self):
        """Starts this Notifier's thread."""
        print('\n[~] Started notifier')
        self.thread.start()

    def _main(self):
        self.ready = True
        self.lastAlertTimeDict = {}
        self.watchlist = {} 
        try:
            config.webhook = SyncWebhook.from_url(NotifSettings('Notifier Settings').get('WebhookURL'))
            user_timezone = pytz.timezone(NotifSettings('Notifier Settings').get('Timezone'))
        except:
            print("Discord Webhook URL or Timezone invalid, notifier disabled")
            return
        flaglist = ["cursed_rune", 
                        "no_damage_numbers", 
                        "map_overcrowded", 
                        "lie_detector_failed",
                        "game_disconnected",
                        "character_dead",
                        "chatbox_msg",
                        "stuck_in_cs",
                        "char_in_town",
                        "player_stuck",
                        "especia_portal"
                        ]

        while True:
            #try except to prevent crashing when user is editing while trying to load configs
            #get user settings
            try:
                suppressAll = NotificationSetting('Notification Settings').get("Suppress_All")
                alertForBotRunning = NotificationSetting('Notification Settings').get("bot_running_toggle")
                for i in flaglist:
                    self.watchlist[i] = {"toggle":NotificationSetting('Notification Settings').get(i+"_toggle"),
                                            "msg":NotificationSetting('Notification Settings').get(i+"_notice")
                                            }
                reviveWhenDead = AutomationParams('Automation Settings').get("revive_when_dead_toggle")
                pauseInTown = AutomationParams('Automation Settings').get("auto_pause_in_town_toggle")
            except:
                pass
            
            if config.enabled and suppressAll != True:
                if alertForBotRunning:
                    alertTextForRunning = NotificationSetting('Notification Settings').get("bot_running_notice")
                    self.alert(config.webhook, user_timezone, self.lastAlertTimeDict, alertTextForRunning, alertCD=300)
                for item in self.watchlist:
                    if getattr(config,item) == True:
                        if self.watchlist[item]["toggle"] == True:
                            alertSent = self.alert(config.webhook, user_timezone, self.lastAlertTimeDict, self.watchlist[item]["msg"])
                            if item == "chatbox_msg" and alertSent:
                                    self.alertFile(target=config.webhook, image="assets\chat.png")
                            if item == "character_dead" and reviveWhenDead:
                                automation.autoRevive()
                            if item == "char_in_town" and pauseInTown:
                                config.listener.toggle_enabled()
            time.sleep(0.5)
    
    def alert(self,target, timezone, alertDict, alertText: str, alertCD = 60):
        """
        Core notification sending engine that manages send frequency
        """
        alertText = str(alertText)
        
        if alertText in alertDict:
            lastAlertSeconds = (datetime.now() - alertDict[alertText]).total_seconds()
            if  lastAlertSeconds > alertCD:   
                alertDict[alertText] = datetime.now()
                alertTextandTime = alertText + " at " + (timezone.localize(datetime.now())).strftime('%d/%m/%Y %H:%M:%S')
                target.send(content=alertTextandTime)
                return True
            else:
                #print("[ALERT  ] Alert CD {:.2f}s: ".format(alertCD - lastAlertSeconds) +alertText)
                return False
        else: 
            alertDict[alertText] = datetime.now()
            alertTextandTime = alertText + " at " + (timezone.localize(datetime.now())).strftime("%d/%m/%Y %H:%M:%S")
            target.send(content=alertTextandTime)
            print("[ALERT  ] Alert sent: "+ alertText)
            return True

    def alertFile(self, target, image):
        path = ".\\" + image
        target.send(file=File(path))