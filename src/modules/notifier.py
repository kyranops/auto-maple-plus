from src.common.interfaces import Configurable
import threading
from discord import SyncWebhook, File
import time
from datetime import datetime
import pytz
from src.gui.notifier_settings.main import NotifSettings
from src.gui.notifier_settings.notification_settings import NotificationSetting
import src.common.config as config

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
        config.webhook = SyncWebhook.from_url(NotifSettings('Notifier Settings').get('WebhookURL'))
        user_timezone = pytz.timezone(NotifSettings('Notifier Settings').get('Timezone'))
        flaglist = ["cursed_rune", 
                        "no_damage_numbers", 
                        "map_overcrowded", 
                        "lie_detector_failed",
                        "game_disconnected",
                        "character_dead",
                        "chatbox_msg",
                        "stuck_in_cs",
                        "player_stuck",
                        "especia_portal"
                        ]

        while True:
            for i in flaglist:
                self.watchlist[i] = {"toggle":NotificationSetting('Notification Settings').get(i+"_toggle"),
                                        "msg":NotificationSetting('Notification Settings').get(i+"_notice")
                                        }
            if config.enabled:
                for item in self.watchlist:
                    if getattr(config,item) == True:
                        if self.watchlist[item]["toggle"] == True:
                            self.alert(config.webhook, user_timezone, self.lastAlertTimeDict, self.watchlist[item]["msg"])
            time.sleep(1)
    
    def alert(self,target, timezone, alertDict, alertText: str):
        """
        Core notification sending engine that manages send frequency
        """
        alertText = str(alertText)
        
        if alertText in alertDict:
            lastAlertSeconds = (datetime.now() - alertDict[alertText]).total_seconds()
            if  lastAlertSeconds > 60:   
                alertDict[alertText] = datetime.now()
                alertTextandTime = alertText + " at " + (timezone.localize(datetime.now())).strftime('%d/%m/%Y %H:%M:%S')
                target.send(content=alertTextandTime)
            else:
                print("[ALERT  ] Alert CD {:.2f}s: ".format(60 - lastAlertSeconds) +alertText)
        else: 
            alertDict[alertText] = datetime.now()
            alertTextandTime = alertText + " at " + (timezone.localize(datetime.now())).strftime("%d/%m/%Y %H:%M:%S")
            target.send(content=alertTextandTime)
            print("[ALERT  ] Alert sent: "+ alertText)