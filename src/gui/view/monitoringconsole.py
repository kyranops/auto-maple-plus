import tkinter as tk
from src.gui.interfaces import LabelFrame


class MonitoringConsole(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Info View', **kwargs)
        print("")

        self.grid_columnconfigure(0, weight=1)

        self.enabledstat = tk.StringVar()
        self.runecdstat = tk.StringVar()
        self.nextcsresetstat = tk.StringVar()
        self.nextexpbuffstat = tk.StringVar()
        self.noOthers = tk.StringVar()
        self.noDmgNo = tk.StringVar()

        self.v0_label = tk.Label(self, text='Bot Enabled Status:')
        self.v0_label.grid(row=0, column=1, padx=5, pady=(5, 0), sticky=tk.E)
        self.v0_entry = tk.Entry(self, textvariable=self.enabledstat, state=tk.DISABLED)
        self.v0_entry.grid(row=0,column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)

        self.v1_label = tk.Label(self, text='Rune Cooldown Status:')
        self.v1_label.grid(row=1,column=1, padx=5, pady=(5, 0), sticky=tk.E)
        self.v1_entry = tk.Entry(self, textvariable=self.runecdstat, state=tk.DISABLED)
        self.v1_entry.grid(row=1,column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)

        self.v2_label = tk.Label(self, text='Time to next EXP Buff:')
        self.v2_label.grid(row=2,column=1, padx=5, pady=(5, 0), sticky=tk.E)
        self.v2_entry = tk.Entry(self, textvariable=self.nextexpbuffstat, state=tk.DISABLED)
        self.v2_entry.grid(row=2, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)

        self.v3_label = tk.Label(self, text='Time to next CS Reset:')
        self.v3_label.grid(row=3,column=1, padx=5, pady=(5, 0), sticky=tk.E)
        self.v3_entry = tk.Entry(self, textvariable=self.nextcsresetstat, state=tk.DISABLED)
        self.v3_entry.grid(row=3,column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)

        self.v4_label = tk.Label(self, text='No. of Other Players:')
        self.v4_label.grid(row=4,column=1, padx=5, pady=(5, 0), sticky=tk.E)
        self.v4_entry = tk.Entry(self, textvariable=self.noOthers, state=tk.DISABLED)
        self.v4_entry.grid(row=4,column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)


    def set_enabledstat(self, string):
        if string == 1:
            self.enabledstat.set("Enabled")
        if string == 0:
            self.enabledstat.set("Disabled")

    def set_runecdstat(self, string):
        self.runecdstat.set(string)

    def set_nextexpbuffstat(self, string):
        self.nextexpbuffstat.set(string)

    def set_nextcsresetstat(self, string):
        self.nextcsresetstat.set(string)

    def set_noOthers(self, string):
        self.noOthers.set(string)