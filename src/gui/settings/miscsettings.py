import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable


class Misc(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Misc. Settings', **kwargs)

        self.cs_settings = MiscSettings('Misc. Settings')
        self.cs_reset_toggle = tk.BooleanVar(value=self.cs_settings.get('cs_reset'))
        self.cs_reset_interval = tk.IntVar(value=self.cs_settings.get('cs_reset_interval'))

        cs_reset_toggle_row = Frame(self)
        cs_reset_toggle_row.pack(side=tk.TOP, fill='x', expand=True, pady=5, padx=5)
        check = tk.Checkbutton(
            cs_reset_toggle_row,
            variable=self.cs_reset_toggle,
            text='Toggle Periodic CS Reset',
            command=self._on_change
        )
        check.pack()

        num_row = Frame(self)
        num_row.pack(side=tk.TOP, fill='x', expand=True, pady=(0, 5), padx=5)
        label = tk.Label(num_row, text='CS Reset Interval:')
        label.pack(side=tk.LEFT, padx=(0, 15))
        radio_group = Frame(num_row)
        radio_group.pack(side=tk.LEFT)
        for i in range(1, 4):
            radio = tk.Radiobutton(
                radio_group,
                text=str(i) + "h",
                variable=self.cs_reset_interval,
                value=i,
                command=self._on_change
            )
            radio.pack(side=tk.LEFT, padx=(0, 10))

    def _on_change(self):
        self.cs_settings.set('cs_reset', self.cs_reset_toggle.get())
        self.cs_settings.set('cs_reset_interval', self.cs_reset_interval.get())
        self.cs_settings.save_config()


class MiscSettings(Configurable):
    DEFAULT_CONFIG = {
        'cs_reset': True,
        'cs_reset_interval': 1
    }