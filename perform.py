##############################
# KIVY MAIN APP CLASSES
##############################
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.core.window import Window
from kivymd.utils import asynckivy as ak
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar

##############################
# KIVYMD Layouts
##############################
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout

##############################
# KIVYMD Widgets
##############################
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton,MDFlatButton,MDRaisedButton,MDRectangleFlatIconButton,MDRectangleFlatButton,MDFloatingActionButton
from kivymd.uix.card import MDCard , MDSeparator
from kivy.properties import StringProperty , DictProperty
from kivymd.uix.list import OneLineListItem, TwoLineListItem , ThreeLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.core.audio import SoundLoader
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.fitimage import FitImage
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.properties import StringProperty

##############################
# MODULES
##############################
import os
import random
import json
from functions import *
import requests
import shutil

with open('appdata.json', 'r') as openfile:
    add_data = json.load(openfile)

class SettingPage(Screen):
    profile_pic = 'Pics/profile.png'
    def enter(self):
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        try:
            self.manager_open = False
            self.file_manager = MDFileManager(
                preview=True,exit_manager=self.exit_manager, select_path=self.select_path
            )
        except:
            toast('Unable to get files information')
        
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
        card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=750)
        card.add_widget(MDLabel(text=f"Profile Pic",halign="center",font_style="H4",bold=True,underline=True,size_hint_y=None,height=100))
        if os.path.exists(self.profile_pic):
            img = FitImage(source=self.profile_pic)
        else:
            img = FitImage(source='Pics/Account.png')
        card.add_widget(img)
        grid = GridLayout(cols=3,size_hint_y=None,height=100)
        grid.add_widget(MDRaisedButton(text="Remove",on_release=lambda x: self.change_profile('remove')))
        grid.add_widget(MDLabel(text=""))
        grid.add_widget(MDRaisedButton(text="Change",on_release=lambda x: self.change_profile('change')))
        card.add_widget(grid)
        self.ids.grid.add_widget(card)
        
        card = MDCard(orientation='horizontal',elevation=5,size_hint_y=None,padding=(50,50),height=200)
        news_topics = ["all",'national','business','sports','world','politics','technology','startup','entertainment','miscellaneous','hatke','science','automobile']
        
        news_items = [{"viewclass": "OneLineListItem","text": f"{i}","height": dp(56),"on_release": lambda x=f"{i}": self.change_news_topic(x),} for i in news_topics] 
        self.news_menu = MDDropdownMenu(
            items=news_items,
            position="center",
            width_mult=4,
        )
        news_topic = add_data["news_topic"]
        card.add_widget(MDLabel(text='News Topic',bold=True))
        self.news_topic_label = MDRaisedButton(text=str(news_topic),on_release=self.news_menu_open)
        card.add_widget(self.news_topic_label)
        self.ids.grid.add_widget(card)
     
    def news_menu_open(self, button):
        self.news_menu.caller = button
        self.news_menu.open()
        
    def change_news_topic(self, text_item):
        with open('appdata.json', 'r') as openfile:
            data = json.load(openfile)
        with open("appdata.json","w") as f:
            data["news_topic"] = text_item
            data = json.dumps(data, indent=4)
            f.write(data)
        self.news_topic_label.text = str(text_item)
        self.news_menu.dismiss()
        
    def change_profile(self, type):
        if type == 'change':
            self.file_test = 'set_profile'
            self.file_manager.show('/storage/emulated/0/')
            self.manager_open = True
            
        elif type == 'remove':
            if os.path.exists('Pics/profile.png'):
                os.remove('Pics/profile.png')
                self.profile_pic = 'Pics/Account.png'
                Snackbar(text='Restart App For better experience').open()
                self.enter()
            else:
                toast('No Profile Pic is There')
        else:
            pass
    
    def select_path(self, path: str):
        try:
            if os.path.isdir(path):
                toast('Choose a file not a folder')
            else:
                if self.file_test == 'set_profile':
                    if os.path.exists('Pics/profile.png'):
                        os.remove('Pics/profile.png')
                    shutil.copy(path,'Pics/profile.png')
                    toast('Profile Made')
                    self.manager_open = False
                    self.profile_pic = path
                    self.file_manager.close()
                    self.enter()
                    Snackbar(text='Restart App For better experience').open()
                else:
                    pass
        except:
            toast('Unable to select file')
            
    def exit_manager(self, *args):
        try:
            self.manager_open = False
            self.file_manager.close()
        except:
            toast('Error no 4 occured')
    
    def home(self):
        self.manager.current = 'homep'