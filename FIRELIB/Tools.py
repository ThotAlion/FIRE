import time

def getTime():
    if sys.platform.startswith('win'):
		return time.clock()
	else:
		return time.time()