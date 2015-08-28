import sys
import subprocess

class Downloader:
	""" intended to manage 'downloading' processes """
	def __init__(self):
		self.processes = []
	
	def download(self, url, filename, wait=False):
		args = ["mplayer", "-dumpfile", filename, "-dumpstream", url]
		#print "args:",args
		proc = subprocess.Popen(args, shell=False,
		                                  stdout=subprocess.PIPE,
		                                  stdin=subprocess.PIPE,
		                                  stderr=subprocess.STDOUT)
		if wait:
			proc.wait()
		else:
			self.processes.append(proc)
		print self.processes
		return
	
#d = Downloader()		
#d.download("http://audio-sv5-t1-2-v4v6.pandora.com/access/716723416285133471.mp3?version=4&lid=888375615&token=BQWdpQdtf5X7SEPMQxtaPQg%2BewCLl0gJiFjIkUJgskTDjt3e5OgxUnDRD6%2Bwb%2B40YFpngZffAeyUl7o1lQ59VcNU4PoNsA%2BxyB8wX1DAEjXAGv0i4S1PjpnUzXP1vkMbD1q%2B3ft7%2Fhf%2F%2FH3ce3Mkt0ulamKd%2Ft2fszvMYBsxmhMAw2ow9J1Kz%2BRKUGKqkrYW75tbRygB%2BIYdDfkcRL5kZZUHqhPgOwuOUUk3RorhHdpaIRCXCqXn2A1YXmxzImQvJWhEc%2FxTvr0OlCB4xnaXk0Ug2xpyeBGDRA8YO5f%2BztjQfpUN3aT5brmr5HWQGflVjjDqiCij%2Bv2PZ%2BN2fxGFYuRTW38AA%2BvgTdBkSn%2FMlgmyebeLUaycsKb9XengiQ%2Fa", "stuff.mp3", wait=True)
	
		

class Player:
	def __init__(self, filename):
		print "initialized player with", filename
		self.length = 0
		args = ['mplayer', '-slave', '-quiet', filename]
		self.proc = subprocess.Popen(args, shell=False,
		                                  stdout=subprocess.PIPE,
		                                  stdin=subprocess.PIPE,
		                                  stderr=subprocess.STDOUT)

	def sendcmd(self, cmd):
		self.proc.stdin.write(cmd.encode("utf-8"))

	def loadfile(self, filename):
		self.length += 1
		cmd = "loadfile {} {}".format(filename, self.length)
		self.sendcmd(cmd)

	def close(self):
		self.proc.kill()

	#def skip(self)
	#	self.sendcmd("

#p = Player('out.mp3')
