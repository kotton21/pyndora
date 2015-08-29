import sys
import subprocess
import select

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
			print '[Downloader]: downloading...'
			proc.wait()
			print '[Downloader]: download complete'
		else:	
			'[Downloader]: running in background'
			self.processes.append(proc)
		#print self.processes
		#return

	
	def close(self):
		for proc in self.processes:
			#proc.stdin.writeline('quit\n') we don't want a half downloaded song.
			proc.wait()
	
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
		#self.proc.stdout.flush()
		sys.stdout.flush()
		ret = []
		while any(select.select([self.proc.stdout.fileno()], [], [], 0.6)):
			ret.append( self.proc.stdout.readline() )
	
	def checkstatus(self):
		print 'checking status'
		length, time = 0, 0
		#purge the output
		while any(select.select([self.proc.stdout.fileno()], [], [], 0.6)):
			ret.append( self.proc.stdout.readline() )
		#get new items
		ret = self.sendcmd('get_property length')
		if len(ret) > 0:
			ret = ret[len(ret)-1].split('=')
			length = ret[len(ret)-1].strip()
		ret = self.sendcmd('get_property time_pos')
		if len(ret) > 0:
			ret = ret[len(ret)-1].split('=')
			time = ret[len(ret)-1].strip()
		print length,time, self.length
		if float(length)-float(time) < 30 or self.length < 3:
			return True
		return False
		
	#if self.length < 4

	# conditions...
	#download when user skips
	#download when next song comes on.

	def sendcmd(self, cmd):
		#TODO player exits at end of playlist, check for dead player, then perform command
		#print cmd,
		#cmd = '{}{}\n'.format( cmd,' '.join(arg for arg in args) )
		print "cmd: [{}]".format(cmd)	
		self.proc.stdin.write(cmd+"\n") #.encode("utf-8")
		if cmd == 'quit':
			return
		else:
			sys.stdout.flush()
			ret = []
			while any(select.select([self.proc.stdout.fileno()], [], [], 0.5)):
				ret.append( self.proc.stdout.readline() )
			return ret
	def loadfile(self, filename):
		print '[Player]: attempting file <{}>'.format(filename)
		print "osaccess",os.access( filename, os.R_OK)
		self.length += 1
		cmd = "loadfile {} {}".format(filename, self.length)
		self.sendcmd(cmd)

	def close(self):
		self.sendcmd('quit')
		#self.proc.kill()

	#def skip(self)
	#	self.sendcmd("

#p = Player('out.mp3')
