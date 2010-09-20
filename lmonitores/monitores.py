#!/usr/bin/env python

#  Author : Umakanthan Chandran ( cumakt@gmail.com )
#  Program : uMonitorES - Ubuntu Monitor Energy Saver
#  Version : 0.1
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#      
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#       
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.


import pygtk
pygtk.require('2.0')
import gtk
import sys
import os
import dbus


from ConfigParser import SafeConfigParser

#REGISTER_KEYCODE1 = 'xmodmap -e "keycode 115 = Super_L"'
#REGISTER_KEYCODE2 = 'xmodmap -e "add mod4 = Super_L"'
GLOBAL_FLAG_MONITOR = 0
SHUTDOWN_MONITOR_CMD = 'xset dpms force off'
LOCK_SYSTEM_CMD = 'xdg-screensaver lock'
SLEEP_CMD = 'sleep 2'
RUN_ADMIN_CMD = 'gksu -'
REGISTER_GCONF_12_KEY = 'gconftool-2 -t str --set /apps/metacity/global_keybindings/run_command_12 "<Control>L"'
REGISTER_GCONF_12_APP = 'gconftool-2 -t str --set /apps/metacity/keybinding_commands/command_12 "/opt/monitores/monitores-ui -shut"'
UNREGISTER_GCONF_12_KEY = 'gconftool-2 -t str --set /apps/metacity/global_keybindings/run_command_12 ""'
UNREGISTER_GCONF_12_APP = 'gconftool-2 -t str --set /apps/metacity/keybinding_commands/command_12 ""'

GET_LAST_UNLOCK = 'cat /var/log/auth.log | grep "gnome-screensaver-dialog: gkr-pam: unlocked \'login\' keyring" | tail -1 | cut -c 1-15'
SETTINGS_CONF = '.settings'

SET_AWAY_ON_PIDGIN = 'purple-remote setstatus?status=away'
D0_NOTHING = 1
	
class OptionWindow(gtk.Window):

   def close_second(self,widget):
       self.window2.destroy()

   def destroyer(self , widget , response_id , data=None):
       widget.hide();
	   
   def message_box(self,message):
       dialog = gtk.MessageDialog(
       parent         = None,
       flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
       type           = gtk.MESSAGE_INFO,
       buttons        = gtk.BUTTONS_OK,
       message_format = message)
       dialog.set_title('Status Window')
       dialog.connect('response', self.destroyer) 
       dialog.show()

   def open_register(self, widget, event, data=None):
       self.window2.destroy()
       dialog = gtk.MessageDialog(
       parent         = None,
       flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
       type           = gtk.MESSAGE_INFO,
       buttons        = gtk.BUTTONS_OK_CANCEL,
       message_format = "This will register shortcut (CTRL+L) for lock Ubuntu , Do you want to continue?")
       dialog.set_title('Popup Window')
       dialog.connect('response', self.register_hotkey)
       dialog.show()        
       return False

   def open_unregister(self, widget, event, data=None):
       self.window2.destroy()
       dialog = gtk.MessageDialog(
       parent         = None,
       flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
       type           = gtk.MESSAGE_WARNING,
       buttons        = gtk.BUTTONS_OK_CANCEL,
       message_format = "This will un-register (CTRL+L) ? Do u want to continue?")
       dialog.set_title('Popup Window')
       dialog.connect('response', self.unregister_hotkey)
       dialog.show()        
       return False

   def register_hotkey(self , widget , response_id , data=None):
       if response_id == gtk.RESPONSE_OK:
           os.system(RUN_ADMIN_CMD)		
           os.system(REGISTER_GCONF_12_KEY)
           os.system(REGISTER_GCONF_12_APP)
           self.message_box('Registered Successfully')
           widget.hide();
       else:
           widget.hide();

   def unregister_hotkey(self , widget , response_id , data=None):
       if response_id == gtk.RESPONSE_OK:
           os.system(RUN_ADMIN_CMD)		
           os.system(UNREGISTER_GCONF_12_KEY)
           os.system(UNREGISTER_GCONF_12_APP)
           self.message_box('UnRegistered Successfully')
           widget.hide();
       else:
           widget.hide();
	   
   def __init__(self, parent=None):
       gtk.Window.__init__(self)
       try:
           self.set_screen(parent.get_screen())
       except:
           self.connect("destroy", lambda *w: gtk.main_quit())
		   
       self.window2 = gtk.Window(gtk.WINDOW_TOPLEVEL)
       self.window2.set_title("Options Here")
       self.window2.set_border_width(10)
       self.window2.set_modal(True)
       self.window2.set_resizable(False)
       box2 = gtk.VBox(False, 10)
       box2.set_border_width(10)
       box2.show()
       button_register = gtk.Button("Register CTRL+L Key")
       button_register.connect_object("clicked", self.open_register,self.window,
                              None)
       button_register.show()	
       box2.pack_start(button_register, True, True, 0)
  
       button_unregister = gtk.Button("UnRegister CTRL+L Key")
       button_unregister.connect_object("clicked", self.open_unregister,self.window,
                              None)
       button_unregister.show()

       box2.pack_start(button_unregister, True, True, 0)
       button2 = gtk.Button("Close")
       button2.connect("clicked", self.close_second)

       box2.pack_start(button2, True, True, 0)	   
       self.window2.add(box2)
       self.window2.show_all()

class MainWindow:
    def set_monitor(self, widget, data=None):
        file = open(SETTINGS_CONF, 'w')
        file.write("1")
        file.close()

    def no_thanks(self, widget, data=None):
        file = open(SETTINGS_CONF, 'w')
        file.write("0")
        file.close()

    def open_option(self, widget, event, data=None):
        OptionWindow()
        return False
		
    def wakeup( self, widget, event, data=None):
        key = gtk.gdk.keyval_name(event.keyval)
        if key == "Escape":
			self.window.hide()
        return False

    def activate( self, widget, data=None):
		self.window.show()
		return False
		
    def hide_window(self, widget, event, data=None):
        self.window.hide()
        return False		
		
    def close_application(self, widget, event, data=None):
        file = open(SETTINGS_CONF, 'w')
        file.write("0")
        file.close()		
        gtk.main_quit()
        return False

    def __init__(self):        
        file = open(SETTINGS_CONF, 'w')
        file.write("1")
        file.close()
				
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
  
        self.window.connect("delete_event", self.close_application)

        self.window.set_title("MonitorES 0.1a")
        self.window.set_border_width(0)
        self.window.set_icon_from_file("/opt/monitores/logo.ico")
        self.staticon = gtk.StatusIcon()
        self.staticon.set_from_stock(gtk.STOCK_EXECUTE)
        self.staticon.connect("activate", self.activate)
        #self.staticon.connect("popup_menu", self.popup)
        self.staticon.set_visible(True)		
        self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.window.connect("key-press-event", self.wakeup)
		
        box1 = gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()

        button = gtk.RadioButton(None, "Monitor Off - Power Saving")
        button.connect("toggled", self.set_monitor, "off")
        button.set_active(True)
        box2.pack_start(button, True, True, 0)
        button.show()

        #button = gtk.RadioButton(button, "Screen Saver On")
        #button.connect("toggled", self.callback, "radio button 2")
        #box2.pack_start(button, True, True, 0)
        #button.show()

        button = gtk.RadioButton(button, "No Thanks")
        button.connect("toggled", self.no_thanks, "radio button 3")
        box2.pack_start(button, True, True, 0)
        button.show()

        separator = gtk.HSeparator()
        box1.pack_start(separator, False, True, 0)
        separator.show()

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, False, True, 0)
        box2.show()

        button = gtk.Button("Settings")
        button.connect_object("clicked", self.open_option, self.window,
                              None)
        box2.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()

        button = gtk.Button("Close To Tray")
        button.connect_object("clicked", self.hide_window, self.window,
                              None)
        box2.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()


        button = gtk.Button("Exit")
        button.connect_object("clicked", self.close_application, self.window,
                              None)
        box2.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()

        self.window.show()

def main():
    gtk.main()
    return 0        

def usage():
    os.system('echo ===== Monitor Energy Saver \(MonitorES\) =====')
    os.system('echo MonitorES is a small utility which help you to turn off monitor \
	display when you lock your machines(CTRL+L)')
    os.system('echo Created by Umakanthan Chandran \(cumakt@gmail.com\)')
		   
if __name__ == "__main__":
	has_argument = False
	action_value = False
	wrong_argument = False
	try:
		if sys.argv[1]:
			getValue = str(sys.argv[1])
			if getValue == "-shut":
				has_argument = True
			else:
				has_argument = True
				wrong_argument = True
				usage()
			#has_argument = True
			file = open(SETTINGS_CONF,"r")
			ret = file.read(1)
			if ret == str("1"):
				action_value = True
			else:
				action_value = False						
	except:
		usage()
    
	#print has_argument
	#print action_value
	#print wrong_argument
	
	if has_argument == True and action_value == True and wrong_argument == False:
		os.system(SLEEP_CMD)
		os.system(SHUTDOWN_MONITOR_CMD)
		os.system(LOCK_SYSTEM_CMD)
		os.system(SET_AWAY_ON_PIDGIN)			
	elif has_argument == False and action_value == False:
		MainWindow()
		main()
	elif has_argument == True and wrong_argument == False:
		D0_NOTHING = 1
	else:
		D0_NOTHING = 1
