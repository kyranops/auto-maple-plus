import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable


class ExpBuff(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'EXP Buff Settings', **kwargs)

        self.expbuff_settings = ExpSettings('EXP Buff Settings')
        self.expbuff_use_toggle = tk.BooleanVar(value=self.expbuff_settings.get('expbuff_use'))
        self.expbuff_use_interval = tk.IntVar(value=self.expbuff_settings.get('expbuff_use_interval'))

        expbuff_use_toggle_row = Frame(self)
        expbuff_use_toggle_row.pack(side=tk.TOP, fill='x', expand=True, pady=5, padx=5)
        check = tk.Checkbutton(
            expbuff_use_toggle_row,
            variable=self.expbuff_use_toggle,
            text='Toggle Use EXP Buff',
            command=self._on_change
        )
        check.pack()

        num_row = Frame(self)
        num_row.pack(side=tk.TOP, fill='x', expand=True, pady=(0, 5), padx=5)
        label = tk.Label(num_row, text='EXP Buff Interval:')
        label.pack(side=tk.LEFT, padx=(0, 15))
        radio_group = Frame(num_row)
        radio_group.pack(side=tk.LEFT)
        for i in range(1,5):
            if i != 3:
                radio = tk.Radiobutton(
                    radio_group,
                    text=str(i*15) + "m",
                    variable=self.expbuff_use_interval,
                    value=i,
                    command=self._on_change
                )
                radio.pack(side=tk.LEFT, padx=(0, 10))

    def _on_change(self):
        self.expbuff_settings.set('expbuff_use', self.expbuff_use_toggle.get())
        self.expbuff_settings.set('expbuff_use_interval', self.expbuff_use_interval.get())
        self.expbuff_settings.save_config()

class ExpSettings(Configurable):
    DEFAULT_CONFIG = {
        'expbuff_use': True,
        'expbuff_use_interval': 2
    }