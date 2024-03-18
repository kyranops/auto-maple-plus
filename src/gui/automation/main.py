import tkinter as tk
from src.gui.interfaces import Tab, LabelFrame
from src.common.interfaces import Configurable

class Automation(Tab):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Automation', **kwargs)

        self.automationSettings = Automation_Settings(self)
        self.automationSettings.pack(side="top", fill="both", padx=5,pady=5)
        self.automationSettings = Autologin_Settings(self)
        self.automationSettings.pack(side="top", fill="both", padx=5,pady=5)


class Automation_Settings(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Triggered Actions', **kwargs)

        #Initialise variable
        self.automation_setting_root = AutomationParams('Automation Settings')
        self.revive_when_dead_toggle = tk.BooleanVar(value=self.automation_setting_root.get("revive_when_dead_toggle"))
        self.auto_cc_toggle = tk.BooleanVar(value=self.automation_setting_root.get("auto_cc_toggle"))
        self.auto_pause_in_town_toggle = tk.BooleanVar(value=self.automation_setting_root.get("auto_pause_in_town_toggle"))
        self.auto_cancel_rune_toggle = tk.BooleanVar(value=self.automation_setting_root.get("auto_cancel_rune_toggle"))

        self.grid_columnconfigure(2, weight=1)
        
        fnlist = {"revive_when_dead":{"toggle": None,"label":"Revive when dead", "params":None, "variables":{"togglestate":self.revive_when_dead_toggle}},
                  "auto_pause_in_town":{"toggle": None,"label":"Auto pause in town (Beta)", "params":None, "variables":{"togglestate":self.auto_pause_in_town_toggle}},
                  "auto_cc":{"toggle": None,"label":"Auto-cc (WIP)", "params":None, "variables":{"togglestate":self.auto_cc_toggle}},
                  "auto_cancel_rune":{"toggle": None,"label":"Auto cancel rune (WIP)", "params":None, "variables":{"togglestate":self.auto_cancel_rune_toggle}}
        }

        for item in fnlist:
            fnlist[item]["toggle"] = tk.Checkbutton(
                                        self,
                                        variable=fnlist[item]["variables"]["togglestate"],
                                        text=fnlist[item]["label"],
                                        command=self._on_change
                                    ).grid(column =0, columnspan=2, padx=5,pady=5, sticky="w")
            if fnlist[item]["params"] != None:
                for parameter in fnlist[item]["params"]:
                    labeltext = tk.Label(self, text=(fnlist[item]["params"][parameter]["paramLabel"]+":"))
                    labeltext.grid(column = 0, padx=5,pady=5, sticky="e")
                    labelrow = labeltext.grid_info()['row']
                    fnlist[item]["params"][parameter]["paramobj"] = tk.Entry(self, textvariable=fnlist[item]["params"][parameter]["var"]).grid(column=1,row=labelrow, padx=5,pady=5)
    def _on_change(self):
        self.automation_setting_root.set('revive_when_dead_toggle',self.revive_when_dead_toggle.get())
        self.automation_setting_root.set('auto_cc_toggle',self.auto_cc_toggle.get())
        self.automation_setting_root.set('auto_pause_in_town_toggle',self.auto_pause_in_town_toggle.get())
        self.automation_setting_root.set('auto_cancel_rune_toggle',self.auto_cancel_rune_toggle.get())
        self.automation_setting_root.save_config()

class Autologin_Settings(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Automatic Login', **kwargs)

        self.automation_setting_root = AutomationParams('Automation Settings')
        #Initialise variable
        self.auto_world = tk.StringVar(value=self.automation_setting_root.get("auto_world"))
        self.auto_login_username = tk.StringVar(value=self.automation_setting_root.get("auto_login_username"))
        self.auto_login2FA_toggle = tk.BooleanVar(value=self.automation_setting_root.get("auto_login2FA_toggle"))
        self.auto_login_pw1 = tk.StringVar(value=self.automation_setting_root.get("auto_login_pw1"))
        self.auto_2FA_secretkey = tk.StringVar(value=self.automation_setting_root.get("auto_2FA_secretkey"))
        self.auto_2ndPW_toggle = tk.BooleanVar(value=self.automation_setting_root.get("auto_2ndPW_toggle"))
        self.auto_2ndPW_pw2 = tk.StringVar(value=self.automation_setting_root.get("auto_2ndPW_pw2"))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        tk.Checkbutton(
                    self,
                    variable=self.auto_login2FA_toggle,
                    text="Auto Login + 2FA",
                    command=self._on_change
                ).grid(row=0, column =0, padx=5,pady=5, sticky="w")
        tk.Checkbutton(
                    self,
                    variable=self.auto_2ndPW_toggle,
                    text="Auto 2nd Password",
                    command=self._on_change
                ).grid(row=0, column =1, padx=5,pady=5, sticky="w")

        tk.Label(self, text="World").grid(row=1, column=0, padx=5, pady=5)
        self.f1 = tk.Entry(self, textvariable=self.auto_world)
        self.f1.grid(row=1,column=1, padx=5, pady=5)
        self.f1.bind("<KeyRelease>",self._on_change)

        tk.Label(self, text="Username").grid(row=2, column=0, padx=5, pady=5)
        self.f1 = tk.Entry(self, textvariable=self.auto_login_username)
        self.f1.grid(row=2,column=1, padx=5, pady=5)
        self.f1.bind("<KeyRelease>",self._on_change)
        tk.Label(self, text="Password").grid(row=3, column=0, padx=5, pady=5)
        self.f2 = tk.Entry(self, textvariable=self.auto_login_pw1, show="*")
        self.f2.grid(row=3,column=1, padx=5, pady=5)
        self.f2.bind("<KeyRelease>",self._on_change)
        tk.Label(self, text="2nd Password").grid(row=4, column=0, padx=5, pady=5)
        self.f3 = tk.Entry(self, textvariable=self.auto_2ndPW_pw2, show="*")
        self.f3.grid(row=4,column=1, padx=5, pady=5)
        self.f3.bind("<KeyRelease>",self._on_change)
        tk.Label(self, text="2FA Secret Key") .grid(row=5, column=0, padx=5, pady=5)
        self.f4 = tk.Entry(self, textvariable=self.auto_2FA_secretkey, show="*")
        self.f4.grid(row=5,column=1, padx=5, pady=5)
        self.f4.bind("<KeyRelease>",self._on_change)
        self.showhidepw_btn = tk.Button(self, text='Show Password', command=self.toggle_password)
        self.showhidepw_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def _on_change(self, *args):
        self.automation_setting_root.set('auto_world',self.auto_world.get().strip())
        self.automation_setting_root.set('auto_login_username',self.auto_login_username.get().strip())
        self.automation_setting_root.set('auto_login2FA_toggle',self.auto_login2FA_toggle.get())
        self.automation_setting_root.set('auto_login_pw1',self.auto_login_pw1.get().strip())
        self.automation_setting_root.set('auto_2FA_secretkey',self.auto_2FA_secretkey.get().strip())
        self.automation_setting_root.set('auto_2ndPW_toggle', self.auto_2ndPW_toggle.get())
        self.automation_setting_root.set('auto_2ndPW_pw2', self.auto_2ndPW_pw2.get().strip())
        self.automation_setting_root.save_config()

    def toggle_password(self):
        if self.f2.cget('show') == '':
            self.f2.config(show='*')
            self.f3.config(show='*')
            self.f4.config(show='*')
            self.showhidepw_btn.config(text = 'Show Password')
        else:
            self.f2.config(show='')
            self.f3.config(show='')
            self.f4.config(show='')
            self.showhidepw_btn.config(text = 'Hide Password')

class AutomationParams(Configurable):
    DEFAULT_CONFIG = {
        'auto_world': "Aquila",
        'revive_when_dead_toggle': False,
        'auto_cc_toggle': False,        
        'auto_pause_in_town_toggle': False,
        'auto_cancel_rune_toggle' : False,
        'auto_login_username':"NULL",
        'auto_login2FA_toggle': False,
        'auto_login_pw1':"NULL",
        "auto_2ndPW_toggle": False,
        "auto_2ndPW_pw2":"NULL",
        "auto_2FA_secretkey":"NULL"
    }