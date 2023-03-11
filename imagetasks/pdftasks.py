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

##############################
# MODULES
##############################
import os
import random
import json
from functions import *
import requests
import time
import logging

class PdfPage(Screen):
    def choose(self, obj):
        try:
            self.manager_open = False
            self.file_manager = MDFileManager(
                preview=True,exit_manager=self.exit_manager, select_path=self.select_path
            )
        except:
            toast('Unable to get files information')
        self.file_manager.show('/storage/emulated/0/')
        self.manager_open = True
    
    def select_path(self, path: str):
        try:
            self.manager_open = False
            self.file_manager.close()
            self.pdf_path = path
            self.make()
        except:
            toast('Unable to select file')
            
    def exit_manager(self, *args):
        try:
            self.manager_open = False
            self.file_manager.close()
        except:
            toast('Error no 4 occured')
    
    def make(self):
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
        path = self.pdf_path
        toast(str(path))
        
    def enter(self):
        try:
            self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
            try:
                self.ids.grid.clear_widgets()
            except:
                pass
            self.ids.grid.add_widget(MDRaisedButton(text='Choose File',pos_hint={'center_x': .5, 'center_y': .5},on_release=self.choose))
        
        except Exception as e:
            toast('Oops! an error occured')
            print(e)
        
    def home(self):
        self.manager.current = 'homep'
        
        
class GoogleDrivePage(Screen):
    def enter(self):
        try:
            self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
            try:
                self.ids.grid.clear_widgets()
            except:
                pass
                
            from auth import get_gdrive_service
            service = get_gdrive_service()
            toast('Authentication Complete')
            
            results = service.files().list(
                pageSize=50, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
            items = results.get('files', [])
            print(items)
            for file in items:
                self.ids.grid.add_widget(MDLabel(text=f"{file['name']}"))
            
            
        except Exception as e:
            toast(f'{e}')
    
    def home(self):
        self.manager.current = 'homep'