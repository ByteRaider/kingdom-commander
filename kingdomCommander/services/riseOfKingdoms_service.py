from . import pywinauto_service
from pywinauto import Application, Desktop
import threading

connected_app = None
        
## Rise of Kingdoms functions
class RiseOfKingdomsBot:
    def __init__(self):
        self.connected_app = None
        self.window = None

    # Connect to Rise of Kingdoms
    def connect_to_rise_of_kingdoms(self):
        self.connected_app = Application(backend="uia").connect(title_re=".*Rise of Kingdoms")
        return self.connected_app

# Singleton instance of the bot
rise_of_kingdoms_bot = RiseOfKingdomsBot()

