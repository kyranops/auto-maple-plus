import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable

class Notification_Settings(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Notification Settings', **kwargs)
       
        #Initialise variable
        self.notification_setting_root = NotificationSetting('Notification Settings')
        self.botrunningNotice = tk.StringVar(value=self.notification_setting_root.get("bot_running_notice"))
        self.botrunningToggle = tk.BooleanVar(value=self.notification_setting_root.get("bot_running_toggle"))
        self.cursedruneNotice = tk.StringVar(value=self.notification_setting_root.get("cursed_rune_notice"))
        self.cursedruneToggle = tk.BooleanVar(value=self.notification_setting_root.get("cursed_rune_toggle"))
        self.NoDmgNotice = tk.StringVar(value=self.notification_setting_root.get("no_damage_numbers_notice"))
        self.NoDmgToggle = tk.BooleanVar(value=self.notification_setting_root.get("no_damage_numbers_toggle"))
        self.overcrowdNotice = tk.StringVar(value=self.notification_setting_root.get("map_overcrowded_notice"))
        self.overcrowdToggle = tk.BooleanVar(value=self.notification_setting_root.get("map_overcrowded_toggle"))
        self.LDfailNotice = tk.StringVar(value=self.notification_setting_root.get("lie_detector_failed_notice"))
        self.LDfailToggle = tk.BooleanVar(value=self.notification_setting_root.get("lie_detector_failed_toggle"))
        self.DCNotice = tk.StringVar(value=self.notification_setting_root.get("game_disconnected_notice"))
        self.DCToggle = tk.BooleanVar(value=self.notification_setting_root.get("game_disconnected_toggle"))
        self.deadNotice = tk.StringVar(value=self.notification_setting_root.get("character_dead_notice"))
        self.deadToggle = tk.BooleanVar(value=self.notification_setting_root.get("character_dead_toggle"))
        self.chatNotice = tk.StringVar(value=self.notification_setting_root.get("chatbox_msg_notice"))
        self.chatToggle = tk.BooleanVar(value=self.notification_setting_root.get("chatbox_msg_toggle"))
        self.stuckInCSNotice = tk.StringVar(value=self.notification_setting_root.get("stuck_in_cs_notice"))
        self.stuckInCSToggle = tk.BooleanVar(value=self.notification_setting_root.get("stuck_in_cs_toggle"))
        self.charInTownNotice = tk.StringVar(value=self.notification_setting_root.get("char_in_town_notice"))
        self.charInTownToggle = tk.BooleanVar(value=self.notification_setting_root.get("char_in_town_toggle"))
        self.playerStuckNotice = tk.StringVar(value=self.notification_setting_root.get("player_stuck_notice"))
        self.playerStuckToggle = tk.BooleanVar(value=self.notification_setting_root.get("player_stuck_toggle"))
        self.playerEspeciaNotice = tk.StringVar(value=self.notification_setting_root.get("especia_portal_notice"))
        self.playerEspeciaToggle = tk.BooleanVar(value=self.notification_setting_root.get("especia_portal_toggle"))
        self.notif_suppression = tk.BooleanVar(value=self.notification_setting_root.get('Suppress_All'))

        #Define layout
        self.grid_columnconfigure(1, weight=1)

        label1 = tk.Label(self, text="Toggle Notification")
        label2 = tk.Label(self, text="Notification Message")
        label1.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        label2.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        tk.Checkbutton(
            self,
            variable=self.botrunningToggle,
            text="Bot Running Normally",
            command=self._on_change
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        n1 = tk.Entry(self, textvariable=self.botrunningNotice)
        n1.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n1.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.cursedruneToggle,
            text="Cursed Rune",
            command=self._on_change
        ).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        n1 = tk.Entry(self, textvariable=self.cursedruneNotice)
        n1.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n1.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.NoDmgToggle,
            text="No Damage Detected",
            command=self._on_change
        ).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        n2 = tk.Entry(self, textvariable=self.NoDmgNotice)
        n2.grid(row=3, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n2.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.overcrowdToggle,
            text="Map Overcrowded",
            command=self._on_change
        ).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        n3=tk.Entry(self, textvariable=self.overcrowdNotice)
        n3.grid(row=4, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n3.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.LDfailToggle,
            text="Lie Detector Failed",
            command=self._on_change
        ).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        n4=tk.Entry(self, textvariable=self.LDfailNotice)
        n4.grid(row=5, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n4.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.DCToggle,
            text="Maplestory Disconnected",
            command=self._on_change
        ).grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        n5=tk.Entry(self, textvariable=self.DCNotice)
        n5.grid(row=6, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n5.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.deadToggle,
            text="Character Dead",
            command=self._on_change
        ).grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        n6=tk.Entry(self, textvariable=self.deadNotice)
        n6.grid(row=7, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n6.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.chatToggle,
            text="Message Detected",
            command=self._on_change
        ).grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        n7=tk.Entry(self, textvariable=self.chatNotice)
        n7.grid(row=8, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n7.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.stuckInCSToggle,
            text="Stuck in Cash Shop",
            command=self._on_change
        ).grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
        n8=tk.Entry(self, textvariable=self.stuckInCSNotice)
        n8.grid(row=9, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n8.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.playerStuckToggle,
            text="Character Stuck",
            command=self._on_change
        ).grid(row=10, column=0, sticky=tk.W, padx=5, pady=5)
        n9=tk.Entry(self, textvariable=self.playerStuckNotice)
        n9.grid(row=10, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n9.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.playerEspeciaToggle,
            text="Especia Portal",
            command=self._on_change
        ).grid(row=11, column=0, sticky=tk.W, padx=5, pady=5)
        n10=tk.Entry(self, textvariable=self.playerEspeciaNotice)
        n10.grid(row=11, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n10.bind("<KeyRelease>",self._on_change)

        tk.Checkbutton(
            self,
            variable=self.charInTownToggle,
            text="Character in Town",
            command=self._on_change
        ).grid(row=12, column=0, sticky=tk.W, padx=5, pady=5)
        n11=tk.Entry(self, textvariable=self.charInTownNotice)
        n11.grid(row=12, column=1, sticky=tk.NSEW, padx=5, pady=5)
        n11.bind("<KeyRelease>",self._on_change)

        muteAll_check = tk.Checkbutton(
            self,
            variable=self.notif_suppression,
            text='Mute All Notifications',
            command=self._on_change
        )
        muteAll_check.grid(column=0, columnspan=2)

    def _on_change(self, *args):
        self.notification_setting_root.set('bot_running_notice', self.botrunningNotice.get())
        self.notification_setting_root.set('bot_running_toggle', self.botrunningToggle.get())
        self.notification_setting_root.set('cursed_rune_notice', self.cursedruneNotice.get())
        self.notification_setting_root.set('cursed_rune_toggle', self.cursedruneToggle.get())
        self.notification_setting_root.set('no_damage_numbers_notice', self.NoDmgNotice.get())
        self.notification_setting_root.set('no_damage_numbers_toggle', self.NoDmgToggle.get())
        self.notification_setting_root.set('map_overcrowded_notice', self.overcrowdNotice.get())
        self.notification_setting_root.set('map_overcrowded_toggle', self.overcrowdToggle.get())
        self.notification_setting_root.set('lie_detector_failed_notice', self.LDfailNotice.get())
        self.notification_setting_root.set('lie_detector_failed_toggle', self.LDfailToggle.get())   
        self.notification_setting_root.set('game_disconnected_notice', self.DCNotice.get())
        self.notification_setting_root.set('game_disconnected_toggle', self.DCToggle.get())
        self.notification_setting_root.set('character_dead_notice', self.deadNotice.get())
        self.notification_setting_root.set('character_dead_toggle', self.deadToggle.get())   
        self.notification_setting_root.set('chatbox_msg_notice', self.chatNotice.get())
        self.notification_setting_root.set('chatbox_msg_toggle', self.chatToggle.get())
        self.notification_setting_root.set('stuck_in_cs_notice', self.stuckInCSNotice.get())
        self.notification_setting_root.set('stuck_in_cs_toggle', self.stuckInCSToggle.get())   
        self.notification_setting_root.set('player_stuck_notice', self.playerStuckNotice.get())
        self.notification_setting_root.set('player_stuck_toggle', self.playerStuckToggle.get())    
        self.notification_setting_root.set('especia_portal_notice', self.playerEspeciaNotice.get())
        self.notification_setting_root.set('especia_portal_toggle', self.playerEspeciaToggle.get())
        self.notification_setting_root.set('char_in_town_notice', self.playerEspeciaNotice.get())
        self.notification_setting_root.set('char_in_town_toggle', self.playerEspeciaToggle.get())
        self.notification_setting_root.set('Suppress_All', self.notif_suppression.get())    
        self.notification_setting_root.save_config()


class NotificationSetting(Configurable):
    DEFAULT_CONFIG = {
        'bot_running_notice': 'NULL',
        'bot_running_toggle': False,        
        'cursed_rune_notice': 'NULL',
        'cursed_rune_toggle': False,
        'no_damage_numbers_notice': 'NULL',
        'no_damage_numbers_toggle': False,
        'map_overcrowded_notice': 'NULL',
        'map_overcrowded_toggle' : False,
        'lie_detector_failed_notice': 'NULL',
        'lie_detector_failed_toggle': False,
        'game_disconnected_notice': 'NULL',
        'game_disconnected_toggle': False,
        'character_dead_notice': 'NULL',
        'character_dead_toggle': False,
        'chatbox_msg_notice': 'NULL',
        'chatbox_msg_toggle': False,
        'stuck_in_cs_notice': 'NULL',
        'stuck_in_cs_toggle': False,
        'char_in_town_notice': 'NULL',
        'char_in_town_toggle': False,
        'player_stuck_notice': 'NULL',
        'player_stuck_toggle': False,
        'especia_portal_notice': 'NULL',
        'especia_portal_toggle': False,
        'Suppress_All': False
    }