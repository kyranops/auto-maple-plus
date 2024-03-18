import tkinter as tk
from src.gui.interfaces import Tab, Frame, LabelFrame
from src.common import config
from src.common.interfaces import Configurable

class Runtime_Flags(Tab):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Monitoring', **kwargs)

        self.runtimeFlags = Runtime_Flags_Frame(self)
        self.runtimeFlags.pack(fill=tk.BOTH, padx=5,pady=5)

class Runtime_Flags_Frame(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Runtime Flags', **kwargs)

        self.enabled_flag = tk.StringVar()
        self.rune_cd_flag = tk.StringVar()
        self.cursed_rune_flag = tk.StringVar()
        self.no_damage_numbers_flag = tk.StringVar()
        self.map_overcrowded_flag = tk.StringVar()
        self.violetta_minigame_flag = tk.StringVar()
        self.lie_detector_failed_flag = tk.StringVar()
        self.game_disconnected_flag = tk.StringVar()
        self.character_dead_flag = tk.StringVar()
        self.chatbox_msg_flag = tk.StringVar()
        self.stuck_in_cs_flag = tk.StringVar()
        self.player_stuck_flag = tk.StringVar()
        self.polo_portal_flag = tk.StringVar()
        self.especia_portal_flag = tk.StringVar()
        self.char_in_town_flag = tk.StringVar()

        flaglist = ["bot_enabled", 
                    "rune_cd", 
                    "cursed_rune", 
                    "no_damage_numbers", 
                    "map_overcrowded", 
                    "violetta_minigame", 
                    "lie_detector_failed",
                    "game_disconnected",
                    "character_dead",
                    "chatbox_msg",
                    "stuck_in_cs",
                    "player_stuck",
                    "especia_portal",
                    "char_in_town"
                    ]
        self.grid_columnconfigure(2, weight=1)

        for i in range(len(flaglist)):
            tk.Label(self, text=flaglist[i]).grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

        self.f1v = tk.Entry(self, textvariable=self.enabled_flag, state=tk.DISABLED).grid(row=0, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f2v = tk.Entry(self, textvariable=self.rune_cd_flag, state=tk.DISABLED).grid(row=1, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f3v = tk.Entry(self, textvariable=self.cursed_rune_flag, state=tk.DISABLED).grid(row=2, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f4v = tk.Entry(self, textvariable=self.no_damage_numbers_flag, state=tk.DISABLED).grid(row=3, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f5v = tk.Entry(self, textvariable=self.map_overcrowded_flag, state=tk.DISABLED).grid(row=4, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f6v = tk.Entry(self, textvariable=self.violetta_minigame_flag, state=tk.DISABLED).grid(row=5, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f7v = tk.Entry(self, textvariable=self.lie_detector_failed_flag, state=tk.DISABLED).grid(row=6, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f8v = tk.Entry(self, textvariable=self.game_disconnected_flag, state=tk.DISABLED).grid(row=7, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f9v = tk.Entry(self, textvariable=self.character_dead_flag, state=tk.DISABLED).grid(row=8, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f10v = tk.Entry(self, textvariable=self.chatbox_msg_flag, state=tk.DISABLED).grid(row=9, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f11v = tk.Entry(self, textvariable=self.stuck_in_cs_flag, state=tk.DISABLED).grid(row=10, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f12v = tk.Entry(self, textvariable=self.player_stuck_flag, state=tk.DISABLED).grid(row=11, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f14v = tk.Entry(self, textvariable=self.especia_portal_flag, state=tk.DISABLED).grid(row=12, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)
        self.f15v = tk.Entry(self, textvariable=self.char_in_town_flag, state=tk.DISABLED).grid(row=13, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)


    def update_All_Flags(self):
        self.enabled_flag.set(str(config.enabled))
        self.rune_cd_flag.set(str(config.rune_cd))
        self.cursed_rune_flag.set(str(config.cursed_rune))
        self.no_damage_numbers_flag.set(str(config.no_damage_numbers))
        self.map_overcrowded_flag.set(str(config.map_overcrowded))
        self.violetta_minigame_flag.set(str(config.violetta_minigame))
        self.lie_detector_failed_flag.set(str(config.lie_detector_failed))
        self.game_disconnected_flag.set(str(config.game_disconnected))
        self.character_dead_flag.set(str(config.character_dead))
        self.chatbox_msg_flag.set(str(config.chatbox_msg))
        self.stuck_in_cs_flag.set(str(config.stuck_in_cs))
        self.player_stuck_flag.set(str(config.player_stuck))
        self.especia_portal_flag.set(str(config.especia_portal))
        self.char_in_town_flag.set(str(config.char_in_town))