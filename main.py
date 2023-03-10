##############################
# KIVY MAIN APP CLASSES
##############################
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.utils import asynckivy as ak
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar

##############################
# KIVYMD Layouts
##############################
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout

##############################
# KIVYMD Widgets
##############################
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout



##############################
# MODULES
##############################
import os 
from os import path
from plyer import stt
from plyer import tts
import random
import json
from android.permissions import request_permissions, Permission
from functions import *
import requests

try:
    if platform == "android":
        request_permissions(
        [
        Permission.INTERNET,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.RECORD_AUDIO,
        Permission.CAMERA
        ]
        )
except:
    ex('Unable to Get Permissions')

lst = ['Pics']
for trip in lst:
    if not os.path.exists(trip):
        os.makedirs(trip)

with open('appdata.json', 'r') as openfile:
    add_data = json.load(openfile)
    
app_title = add_data['title']
app_desc = add_data['description']


##############################
# CLASSES OF SCREENS
##############################
from home import HomePage
from perform import SettingPage

class MainApp(MDApp):
    def build(self):
        Window.bind(on_keyboard=self.key_input)
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M2"
        
        self.set_bars_colors()
        
        Builder.load_file('perform.kv')
        
        sm=ScreenManager()
        sc_lst = [
        HomePage(name='homep'),
        SettingPage(name='settp')
        ]
        for sc in sc_lst:
            sm.add_widget(sc)
            
        return sm

    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primary_color, 
            self.theme_cls.primary_color,
            "Light",
        )
        
    def key_input(self, window, key, scancode, codepoint, modifier):
      if key == 27:
          print('Pressed back button')
      else:
         return False

MainApp().run()