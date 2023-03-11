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

class HomePage(Screen):
    news_data = None
    def enter(self):
        self.ids.loader.active = True
        with open('appdata.json', 'r') as openfile:
            add_data = json.load(openfile)
        app_title = add_data['title']
        app_desc = add_data['description']
        
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        try:
            if os.path.exists('Pics/profile.png'):
                self.ids.ttool.source = f'Pics/profile.png'
            else:
                self.ids.ttool.source = f'Pics/Account.png'
        except:
            toast('Unable to set Profile')
        
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
        self.ids.tbar.title = app_title
        self.ids.ttool.title = app_title
        self.ids.ttool.text = app_desc
        
        try:
            from bs4 import BeautifulSoup
            weat_url = 'https://www.google.com/search?q=varanasi+weather'
            r = requests.get(weat_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            html = soup.prettify()
                
            asl = soup.find_all('div')
            lst = []
            for x in asl:
                lst.append(x.get_text())
                    
            we = lst[26].replace('HazeMore on weather.com','')
            wel = we.split('/')
            weather = wel[1].replace(' ','')
            weather = weather.split(f'C')[0] + f'C'
            weather = weather.replace('eather','eather ')
            place = wel[0]
            
            card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=300)
            card.add_widget(MDLabel(text=f"{place} {weather}",bold=True))
            ct = time.localtime()
            dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
            tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
            self.time_label = MDLabel(text=f"Date - {dt}      Time - {tt}",bold=False)
            card.add_widget(self.time_label)
            self.ids.grid.add_widget(card)
            try:
                ak.start(self.update_time())
            except Exception as e:
                toast(str(e))       
        except Exception as e:
            toast('Unable to get weather data')
            toast(f'{e}')
            
        card = MDCard(orientation='vertical',elevation=5,size_hint_y=None,padding=(50,50),height=750)
        topic = add_data["news_topic"].split('news?category=')[-1].capitalize()
        card.add_widget(MDLabel(text=f"{topic} News",halign="center",font_style="H4",bold=True,underline=True,size_hint_y=None,height=100))
        self.news_label = MDLabel(text=f"No News Is There",halign="center")
        card.add_widget(self.news_label)
        grid = GridLayout(cols=3,size_hint_y=None,height=100,padding=(0,20),spacing=(50,0))
        grid.add_widget(MDRaisedButton(text="Previous",on_release=lambda x: self.change_news('previous')))
        grid.add_widget(MDRaisedButton(text="Refresh",on_release=lambda x: self.change_news('refresh')))
        grid.add_widget(MDRaisedButton(text="Next",on_release=lambda x: self.change_news('next')))
        card.add_widget(grid)
        self.ids.grid.add_widget(card)
        
        try:
            self.news_number = 1
            ak.start(self.make_news())
        except Exception as e:
            toast(str(e))
        self.ids.loader.active = False
    
    
    async def update_time(self):
        for x in range(300):
            await ak.sleep(1)
            ct = time.localtime()
            dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
            tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
            self.time_label.text = f"Date - {dt}      Time - {tt}"
        
    async def make_news(self):
        num = 0
        with open('appdata.json', 'r') as openfile:
            add_data = json.load(openfile)
        if self.news_data == None:
            num = 1
            res = requests.get(add_data["news_api"] + add_data["news_topic"])
            data = res.json()
            self.total_news = len(data["data"])
            self.news_data = data
        else:
            data = self.news_data
        if data == {} and num == 1:
            num = 2
            print('Second try on news data')
            ak.start(self.make_news())
        n = 0
        for cont in data["data"]:
            n = n + 1
            news = cont["content"]
            if n == self.news_number:
                break
        self.news_label.text = str(news)
    
    def change_news(self, type):
        if type == 'next':
            if self.news_number==self.total_news:
                toast('All News Finished')
            else:
                self.news_number = self.news_number + 1
                ak.start(self.make_news())
        elif type == 'refresh':
            toast('Refreshing...')
            self.news_data = None
            self.news_number = 1
            ak.start(self.make_news())
        else:
            if self.news_number == 1:
                toast('This is the first news')
            else:
                self.news_number = self.news_number - 1
                ak.start(self.make_news())
    
    def goto(self, where):
        self.manager.current = where
    
    def tell(self, text):
        toast(str(text))