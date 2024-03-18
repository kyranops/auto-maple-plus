import tkinter as tk
from src.gui.interfaces import Tab, Frame, LabelFrame
from src.common import config
from src.gui.notifier_settings.notification_settings import Notification_Settings
from src.common.interfaces import Configurable
import datetime

class Notifier_Settings(Tab):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Notifier', **kwargs)

        self.noti_target = Notification_Target(self)
        self.noti_target.pack(fill=tk.BOTH ,padx=5,pady=5)
        self.noti_settings = Notification_Settings(self)
        self.noti_settings.pack(fill=tk.BOTH, padx=5,pady=5)

class Notification_Target(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Notification Target', **kwargs)
        self.grid_columnconfigure(1, weight=1)

        self.notif_settings_root = NotifSettings('Notifier Settings')
        self.webhook_url = tk.StringVar(value=self.notif_settings_root.get('WebhookURL'))
        self.timezone = tk.StringVar(value=self.notif_settings_root.get('Timezone'))

        self.discordWebhookLabel = tk.Label(self, text="Discord Webhook URL")
        self.discordWebhookLabel.grid(row = 0, column = 0, sticky=tk.NSEW, padx=5, pady=5)
        self.discordWebhookEntry = tk.Entry(self, textvariable=self.webhook_url)
        self.discordWebhookEntry.bind("<KeyRelease>",self._on_change)
        self.discordWebhookEntry.grid(row = 0, column = 1, sticky=tk.NSEW, padx=5, pady=5)
        self.discordTimezoneLabel = tk.Label(self, text="Timezone")
        self.discordTimezoneLabel.grid(row = 1, column = 0, sticky=tk.NSEW, padx=5, pady=5)
        self.discordTimezoneEntry = tk.Entry(self, textvariable=self.timezone)
        self.discordTimezoneEntry.bind("<KeyRelease>",self._on_change)
        self.discordTimezoneEntry.grid(row = 1, column = 1, sticky=tk.NSEW, padx=5, pady=5)

        self.testMessage = tk.Button(self, text="Send Test Notification", command=self._send_test_notification).grid(row = 2, column=0, columnspan=2, padx=5, pady=5)

    def _on_change(self, *args):
        self.notif_settings_root.set('WebhookURL', self.webhook_url.get())
        self.notif_settings_root.set('Timezone', self.timezone.get())
        self.notif_settings_root.save_config()

    def _send_test_notification(self):
        alertTextandTime = "Webhook Test Successful"
        config.webhook.send(content=alertTextandTime)


class NotifSettings(Configurable):
    DEFAULT_CONFIG = {
        'WebhookURL': 'NULL',
        'Timezone': 'UTC'
    }
    