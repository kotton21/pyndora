import pandora
import sys
import subprocess
import os
import threading
import csv
import pickle
from time import sleep

execfile("Downloader.py")

SETTINGS_FILE = "config.pickle"

def loadSettings(filename):
	''' loads the settings from a .pickle file '''
	try:
		with open(filename,'rb') as f:
			settings = pickle.load(f)
	except IOError:
		print "Could not open default settings file"
		settings = {'un':'upbeatlodown@gmail.com',
				'pw':'fuckmicah',
				'lastStation':"The Glitch Mob Radio",
				'songs_file':"songs.pickle",
				'songs_path':'music/'}
	return settings

class Song:
	def __init__(self, name, artist, album, filename, rate, codec):
		self.name = name
		self.artist = artist
		self.album = album
		self.filename = filename
		self.rate = rate
		self.codec = codec

def getSong():
	songdict = pan.get_next_song()
	#print songdict
	name = songdict['artistName'] + '-' + songdict['songName']
	forbidden = "\n,.\t\"\'/?:|~"
	newname = ''.join(l for l in name if l not in forbidden)

	song = Song(songdict['songName'],
					songdict['artistName'],
					songdict['albumName'],
					newname.replace(' ','_')+'.mp3',
					None,
					None)
	url = songdict['audioUrlMap']['highQuality']['audioUrl']
	return (song, url)

"""
def updatePStatus():
        '''simply prints the status of the player on screen, not functionally required''' 
        try:
            out = player.stdout
            while(True):
                subsystemOut = out.readline().decode("utf-8")
                if subsystemOut == '':
                    break
                subsystemOut = subsystemOut.strip()
                subsystemOut = subsystemOut.replace("\r", "").replace("\n", "")
                print "[ Player ] : "+subsystemOut
	except:
		print "[ Player ] : error updating status"

def updateDStatus():
        '''simply prints the status of the downloader on screen, not functionally required'''
        try:
            out = downloader.stdout
            while(True):
                subsystemOut = out.readline().decode("utf-8")
                if subsystemOut == '':
                    break
                subsystemOut = subsystemOut.strip()
                subsystemOut = subsystemOut.replace("\r", "").replace("\n", "")
                print "[ Downloader ] : "+subsystemOut
	except:
		print "[ Downloader ] : error updating status"
"""
	
pan = pandora.Pandora()
settings = loadSettings(SETTINGS_FILE)

pan.authenticate(settings['un'],settings['pw'])

raw = settings['lastStation']
newStation  = ""

#def getStation(stationName):
for station in pan.stations:
	if raw == station['stationName']: # or raw_i == station['topStationsSortIndex']:
		newStation = station

pan.switch_station(newStation)

if pan.current_station is None:
	print "That's not a staton, please try agagin"
	sys.exit()

'''
playeropts = ["cvlc", "--intf=rc"] #--sout-display-audio , "--quiet"
player = subprocess.Popen(playeropts, shell=False,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
t_player = threading.Thread(target=updatePStatus, args=())
t_player.Daemon = True
t_player.start()


class CVLC():
	def __init__(self, name):
		self.name = name
		#start the trhead to update staus
	def download(self):
		pass
	def play(self, filename):
		pass
	def updateStatus(self):
		pass
	def close(self):
		pass
'''
#songs = loadSongs(settings['songs_file'])		

"""
downloader = None
def download(song, url, downloader):
	#TODO kill the downloader status updater
	# then reset

	#reset downloader
	if downloader is not None:
		os.kill(downloader.pid, 15)
		downloader.wait()
		downloader = None
		print 'downloader killed'

	print 'resetting downloader'
	# reset downloader
	arg = '--sout=file/mp3:'+settings['songs_path']+song.filename
	#print arg
	#print 'URL...... ', url
	#print 'arg.....', arg
	opts = ["cvlc", url, arg] #--sout-display-audio, "--quiet"
	#print opts
	downloader = subprocess.Popen(opts, shell=False,
		                                  stdout=subprocess.PIPE,
		                                  stdin=subprocess.PIPE,
		                                  stderr=subprocess.STDOUT)

	#t_downloader = threading.Thread(target=updateDStatus, args=())
	#t_downloader.Daemon = True
	#t_downloader.start()
	print "downloader reset"
"""

d = Downloader()	
song,url = getSong()
print 'enqueued new song',song.artist,',',song.name
print url
d.download(url, settings['songs_path']+song.filename, wait=True)
p = Player( settings['songs_path']+song.filename )

"""
def playerAdd(filename):
	sendPlayer('enqueue', filename)
def sendPlayer(cmd, arg=''):
	cmd = cmd+" "+arg+"\n"
	player.stdin.write(cmd.encode("utf-8"))
"""

def enqueueNewSong(d):
	song,url = getSong()
	d.download(url, settings['songs_path']+song.filename, wait=False)
	#playerAdd(settings['songs_path']+song.filename)
	p.loadfile(settings['songs_path']+song.filename)
	print 'enqueued new song',song.artist,',',song.name
	print url
	#sendPlayer('play')
	return

#enqueueNewSong(d)
'''
newsong,url = getSong()
arg = '--sout=file/mp3:'+settings['songs_path']+newsong.filename
#print arg
#print 'URL...... ', url
#print 'arg.....', arg
opts = ["cvlc", url, arg] #--sout-display-audio, "--quiet"
#print opts
downloader = subprocess.Popen(opts, shell=False,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)

t_downloader = threading.Thread(target=updateDStatus, args=())
t_downloader.Daemon = True
t_downloader.start()
'''
#timer_downloader = Timer..
#def reset
#	close last thread, cancel the updateStatus thread and kill the process... 
# 	start another process

'''
archivedSong = findSong(songs, newsong.name, newsong.artist)
if archivedSong is None:
	songs.append(newsong)
'''
#on startup:
#load full first song into buffer direcotry
# play songs from that direcoty?
# would need an instance of cvlc to download, and another to play
# buffer directory should number the songs so that they are loaded up in order
# on saving, copy to proper directory, without the order number
# Check that the file doesn't already exist...
# 
"""
def CheckPlayerStatus():
	#TODO race conditions
	#TODO will constantly update if song is paused less than 30
	#t_player.
	print "checking player status"
	def getPlayerOut():
		out = player.stdout
		while(True):
			subsystemOut = out.readline().decode("utf-8")
			if subsystemOut == '':
				break
			subsystemOut = subsystemOut.strip()
			subsystemOut = subsystemOut.replace("\r", "").replace("\n", "").replace("> ","")
			print "[ Player subsystem ] : "+subsystemOut
		return subsystemOut
	#except:
	#print "[ Player ] : error updating status"
	getPlayerOut()
	sendPlayer('get_length')
	length = getPlayerOut()
	sendPlayer('get_time')
	time = getPlayerOut()
	print 'stat: {} of {}'.format(time,length)
	if int(length) - int(time) < 30:
		enqueueNewSong(d)
	
	t_download = threading.Timer(30, CheckPlayerStatus)
	

t_download = threading.Timer(.01, CheckPlayerStatus)
t_download.Daemon = True
t_download.start()
"""
print "enter vlc commands"
try:
	while True:

		raw = raw_input("> ")
		if raw == "":
			print "getting song"
			enqueueNewSong(d)
		elif raw == "p":
				cmd = "p"
				p.sendcmd(cmd)
		else:
			print "cmd: [{}]".format(raw)
			p.sendcmd(raw+"\n")
			#for line in player.stdin:
			#	print line.readline().decode("utf-8")
except KeyboardInterrupt as ex:
	print ex.args

try:
	with open(SETTINGS_FILE, 'wb+') as f:
		pickle.dump(settings,f)
except IOError:
	print 'could not save settings file'
'''
try:
	with open(settings['songs_file'], 'wb+') as f:
		pickle.dump(songs, f)
except IOError:
	print 'could not savedata1 songs file'
'''

"""
if player is not None:
	os.kill(player.pid, 15)
	player.wait()
	player = None
	print 'player killed'
if downloader is not None:
	os.kill(downloader.pid, 15)
	downloader.wait()
	downloader = None
	print 'downloader killed'
#subprocess terminate
"""
p.close()
pan.terminate()


