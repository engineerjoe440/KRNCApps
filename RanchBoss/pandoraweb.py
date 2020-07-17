#!/usr/bin/python3

#########################################################################################
# Python Bottle Web Application
# Used for interfacing with Pianobar Pandora-Client on a Raspberry Pi.
# Written by Joe Stanley
# (c) Stanley Solutions
#########################################################################################

import os
import socket
import threading

def rpiip():
    return((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname('/home/pi/pandoraweb/pandoraweb.py'))

from bottle import route, run, template, get, post, Bottle
from bottle import request, error, static_file, redirect

# Define Webpage Parameters
IP = rpiip() # Capture Defined IP
PORT = '8080'
HTMLdir = "/home/pi/pandoraweb"
IMGdir = "/home/pi/pandoraweb/Images"
music_playing = False

Webapp = Bottle()

# Define and route Static Files (Images):
@Webapp.route('/settings/<filename>')
@Webapp.route('/setting/<filename>')
@Webapp.route('/index/<filename>')
@Webapp.route('/<filename>')
def server_static(filename):
    return(static_file(filename, root=IMGdir))

# Define Pages:
def home(songinfo):
    return( template("index.tpl", {'songinfo':songinfo}, root=HTMLdir) )
def settings(songinfo):
    return( template("settings.tpl", {'songinfo':songinfo}, root=HTMLdir ) )

# Define Terminal Interaction Function
def cmd( command ):
    # Send command to Terminal
    os.system( command )

# Define Pianobar Control Function:
def pianobar( command ):
    # Generate Command String
    command = "echo '" + command + "' >> /home/pi/.config/pianobar/ctl"
    # Send command to Terminal
    cmd( command )

# Define timer Control Function
def timer():
    if not music_playing:
        pianobar( "q" )
        cmd( "sudo killall pianobar" )
    
# Define Play/Pause Conditioner Function
def playpausecond():
    global music_playing
    # Check for running Pianobar Process
    if( os.system("pidof pianobar") == 0 ):
        # Pianobar process is running
        pianobar("p") # Send Play/Pause Command
        if(music_playing): # Pause Requested
            threading.Timer(100, timer).start()
        music_playing = not music_playing
    else:
        # No Running Process, Must Start One
        music_playing = True
        cmd( "nohup pianobar > pianobar.out 2>&1 &" )

# Define Generic GET-Based Homepage-Load:
@Webapp.route('/index')
@Webapp.route('/')
def index():
    return( home(str(music_playing)) )

# Define Generic GET-Based Settings-Load:
@Webapp.route('/settings')
@Webapp.route('/setting')
def settingspage():
    return( settings( str(music_playing) ) )

# Define Control-Based Function
@Webapp.post('/index')
@Webapp.post('/')
def home_control():
    global music_playing
    
    playpauseid   = request.forms.get('playpause')
    skipid        = request.forms.get('skip')
    settingid     = request.forms.get('settings')
    stationlistid = request.forms.get('stationlist')
    vdownid       = request.forms.get('vdown')
    vupid         = request.forms.get('vup')
    thumbdownid   = request.forms.get('thumb_down')
    thumbupid     = request.forms.get('thumb_up')
    tiredid       = request.forms.get('tired')
    
    # Send Pianobar command as necessary
    if(playpauseid!=None):      playpausecond()
    elif(skipid!=None):         pianobar("n")
    elif(vdownid!=None):        pianobar("(((((")
    elif(vupid!=None):          pianobar(")))))")
    elif(thumbdownid!=None):    pianobar("-")
    elif(thumbupid!=None):      pianobar("+")
    elif(tiredid!=None):        pianobar("t")
    
    # Change page as necessary
    if(settingid!=None):        redirect("/setting")
    elif(stationlistid!=None):  redirect("/stations")
    else:                       return(home(str(music_playing)))

@Webapp.post('/settings')
@Webapp.post('/setting')
def setting_control():
    global music_playing
    
    returnid      = request.forms.get('return')
    playpauseid   = request.forms.get('playpause')
    start         = request.forms.get('start')
    stop          = request.forms.get('stop')
    reboot        = request.forms.get('reboot')
    
    # Perform Desired Action
    if(start!=None):
        cmd( "nohup pianobar > pianobar.out 2>&1 &" )
        music_playing = True
    if(stop!=None):
        pianobar( "q" )
        cmd( "sudo killall pianobar" )
        music_playing = False
    if(reboot!=None):
        cmd( "sudo reboot" )
    
    if(playpauseid!=None):
        playpausecond()
        return(settings(str(music_playing)))
    else:
        redirect("/")

@Webapp.error(404)
def error404(error):
    return( template("404err.tpl", root=HTMLdir ) )

# Run the Server
Webapp.run(host=IP, port=PORT, reloader=True)
