# accounts/apps.py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'microblogging'
    verbose_name = 'microblogging'

    def ready(self):
        from . import signals