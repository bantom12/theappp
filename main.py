
import shutil
from kivy.uix.boxlayout import BoxLayout




import sys
import lzma
import tempfile



from struct import pack


from construct import *




import logging
from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout

# Configure Python logging to capture Kivy logs


# Now Kivy logs will be captured by Python logging








import os
from kivy.uix.popup import Popup



import traceback

import praw
from kivy.uix.image import Image
import random
import re


from kivy.app import App
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button



from kivy.utils import get_color_from_hex


from kivy.graphics import Rectangle, Color





GMA_VERSION = b"\x03".decode("utf-8")

GMAFile = "all_file_meta" / Struct(
    "file_number" / Int32ul,
    "data"
    / IfThenElse(
        this.file_number != 0,
        "data"
        / Struct(
            "file_name" / CString("utf8"), "file_size" / Int64sl, "file_crc" / Int32ul
        ),
        Pass,
    ),
)



class FileContents(Adapter):
    def _encode(self, obj, context, path):
        return b"".join(obj)

    def _decode(self, obj, context, path):
        contents = []
        begin = 0
        for filemeta in context._.all_file_meta:
            # ignore the dummy file with file number 0
            if filemeta.file_number == 0:
                break

            size = filemeta.data.file_size
            contents.append(obj[begin : begin + size])
            begin += size

        return contents
        
        
def file_content_size(context):
    total = 0
    for filemeta in context.all_file_meta:
        if filemeta.file_number == 0:
            return total

        total += filemeta.data.file_size




GMAContents = "content" / Struct(
    "signature" / Const(b"GMAD"),
    "format_version" / PaddedString(1, "utf8"),
    "steamid" / Int64sl,
    "timestamp" / Int64sl,
    "required_content" / CString("utf8"),
    "addon_name" / CString("utf8"),
    "addon_description" / CString("utf8"),
    "addon_author" / CString("utf8"),
    "addon_version" / Int32sl,
    # For each file get the metadata
    "all_file_meta" / RepeatUntil(lambda x, lst, ctx: x["file_number"] == 0, GMAFile),
    "total_file_size" / Computed(lambda ctx: file_content_size(ctx)),
    "embedded_files"
    / LazyStruct("contents" / FileContents(Bytes(this._.total_file_size))),
)

GMAVerifiedContents = "GMAVerifiedContents" / Struct(
    GMAContents,
    "addon_crc" / Optional(Int32ul),
    "MagicValue" / Optional(Int8ul)
    # Don't enforce terminator. Some GMA files appear to have 0-padding after the magic value
    # Terminator
)

GMAVerifiedContents = "GMAVerifiedContents" / Struct(
    GMAContents,
    "addon_crc" / Optional(Int32ul),
    "MagicValue" / Optional(Int8ul)
    # Don't enforce terminator. Some GMA files appear to have 0-padding after the magic value
    # Terminator
)






class MyPopup(Popup):
    def __init__(self, **kwargs):
        
        self.title = 'Gmad Extractor'
        
        super(MyPopup, self).__init__(**kwargs)
        self.label = Label(text="\n\n\nApp created by: BOO-49\n\n"
                                   "Instructions:\n"
                                   "1. make sure to grant access files permission\n"
                                   "2. put your .gma file directory and PRESS submit.\nnot enter on the keyoard.\n"
                                   "3. wait, extracted files will be compressed in\n Boo_extracted folder.\n"
                                  
                                   "if you got an error, contact me.\n //discord : boo271"
                             
                                  
                                   , pos_hint = {'center_x': 0.50, 'center_y': 0.67}, color=get_color_from_hex('#00ff00'), font_size=34)
                                   
        self.size_hint=(None, None)                           
        self.size=(840, 620)
        self.content = BoxLayout()
        self.content.add_widget(self.label)
       

      # Change color to red
        
        
        
            
            




class MyApp(App):
    def build(self):
           layout = FloatLayout()
           bg_pic = Image(source='minimal-skull-art.jpg', allow_stretch=True)
           layout.add_widget(bg_pic)
        
           
           self.input_box = TextInput(hint_text='Path To The .Gma File.',
                                    background_color=(1,1,1,1))
           self.input_box.size_hint = (None, None)
           self.input_box.size = (600, 60)  
           
           self.input_box.pos_hint = {'center_x': 0.50, 'center_y': 0.80}  # Position at the center of the layout
           self.input_box.bind(on_text_validate=self.on_button_press)
           
        
                                   
        
           
           self.submit_button = Button(text='Submit', size_hint=(0.2, None), height=80)
           self.submit_button.pos_hint = {'center_x': 0.50, 'center_y': 0.2}  # Position in the center
           self.submit_button.bind(on_press=self.on_button_press)
           self.submit_button.background_color=(1,1,1,1)
           button11= Button(text='info', pos_hint = {'center_x': 0.90, 'center_y': 0.97}, size_hint=(None,None,), size=(100, 50), background_color=(0,0,0,0))
           button11.bind(on_release=self.colot_change)
           self.label = Label()
           self.label.text= ''
           self.label.pos_hint = {'center_x': 0.50, 'center_y': 0.87}
           
           
           
          
           
           
           layout.add_widget(self.input_box)
           layout.add_widget(self.submit_button)
           layout.add_widget(button11)
           layout.add_widget(self.label)
           
           
           
           return layout
           return info_button
           
         

    def colot_change(self, instance):
           	popup = MyPopup()
           	popup.open()
        
           	
           	
           	
           
    def on_button_press(self, instance):
     
        user_input = self.get_user_input().replace('\n', '')
     
        self.your_function(user_input)
    
    def get_user_input(self):
       
        return self.input_box.text
    
    def your_function(self, value):
        value.replace('\n', ' ')
        try :
        	self.label.text = 'Please Wait.'
        	
        	with open(value, "rb") as file:
        		gma = GMAVerifiedContents.parse_stream(file)
        		from pathlib import Path
        		folder_path = Path('/sdcard/extracted')
        		folder_path.mkdir(parents=True, exist_ok=True)
        		for i in range(0, len(gma.content.all_file_meta) - 1):
        			meta = gma.content.all_file_meta[i]
        			gma_file_name = meta.data.file_name
        			
        			file_name = os.path.join('/sdcard/extracted', gma_file_name)
        			file_folder = os.path.dirname(file_name)
        			if not os.path.exists(file_folder):
        					os.makedirs(file_folder)
        			with open(file_name, "wb") as output:
        					output.write(gma.content.embedded_files.contents[i])
        			dirrr = os.path.join('/sdcard/Boo_extrated')
        			if not dirrr:
        				self.label.text="nkskshsjsjsjshs"
        				return
        				
        				
        					
        					
        		
        		wow = value.split('/')[-1]
        		woww = wow.split('.')[-2]
        		
        		shutil.make_archive(f'/sdcard/Boo_extracted/{woww}', 'zip', '/sdcard/extracted')
        		
        		
        		
        		
        		for root, dirs, files in os.walk('/sdcard/extracted', topdown=False):
        			for name in dirs:
        				folder_path = os.path.join(root, name)
        				shutil.rmtree(folder_path)
        			for jj in files:
        				intok = os.path.join(root, jj)
        				os.remove(intok)
        		self.label.color=get_color_from_hex("00ff00")
        		self.label.text="Extracted Successfully ! Saved to /sdcard/Boo_extracted "
    					
    					
        			
    				
    					
    				
    					
    					
    			
        		 
        			
        					
        					
        	 
        				
        		

        					

        			
        					
        except :
        					self.label.color = get_color_from_hex("ff0000")
        					self.label.text="Error, make sure to put the right Directory, then try again."
        					
        					return
        					
        
        			
        			
        			
        			
        				
        				

    
    
        
        

if __name__ == '__main__':
    MyApp().run()
logging.basicConfig(level=logging.DEBUG)

# Redirect Kivy logs to Python logging
Logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

        			
        
       
        	
