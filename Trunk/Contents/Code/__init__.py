"""
 Plex plugin for watching online-Episodes of the


@version V0.9
@author Philipp Ringel
@url http://code.google.com/p/plex-rtlnow/

"""

from htmlentitydefs import entitydefs
import urllib
import urllib2
import re
import base64
import ExceptionHandler
import RTLNowParser
import urllib2_new

PLUGIN_PREFIX = "/video/RTLNetwork"
MainArt         = "%s/RTLNow/:/resources/%s" % (PLUGIN_PREFIX, "rtlnow-art-default.png")
MainThumb       = "%s/RTLNow/:/resources/%s" % (PLUGIN_PREFIX, "rtlnow-icon-default.png")

############################################################################################################
#
#  Start Routine
#
#  Initialization of the Plugin
#
###########################################################################################################
def Start():

	# Set up view groups
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	Plugin.AddViewGroup("Info", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("Details", viewMode="PanelStream", mediaType="items")

	HTTP.CacheTime = 3600
	HTTP.Headers['User-agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10'

	# Set the default MediaContainer attributes
	#MediaContainer.title1 = 'RTL Network'
	#MediaContainer.content = 'List'
	#MediaContainer.art = MainArt


###########################################################################################################
#
#  Main Menu Routines
#
#  Main Menu Definitions
#
###########################################################################################################
@handler('/video/RTLNetwork/RTLNow', 'RTL Now', thumb="rtlnow-icon-default.png", art="rtlnow-art-default.png")
def MainMenuRtlNow():
	"""
	Main Routine for Displaying the Main Menu of RTL Now
	"""
	try:
		parser = RTLNowParser.RTLNowParser()
		return parser.getGenres()
	except urllib2_new.URLError, e:
		return MessageContainer('Network Error', 'Please check your Internet-Connection!')
	except Exception, e:
		handler = ExceptionHandler.ExceptionHandler(e)
		return handler.getBailOut()

#@handler('/video/RTLNetwork/SuperRtl', 'Super RTL', thumb="superrtlnow-icon-default.png", art="superrtlnow-art-default.png")
def MainMenuSuperRtlNow():
	"""
	Main Routine for Displaying the Main Menu of RTL Now

	Not implemented yet...
	"""
	try:
		parser = RTLNowParser.RTLNowParser()
		return parser.getGenres()
	except Exception, e:
		return MessageContainer("Error getting Genres!", L(e))

###########################################################################################################
#
#  Sub Menu Routines
#
#  Sub Menu Definitions
#
###########################################################################################################
def ShowsList(parserType = None, url = None):
	try:
		if parserType == 'RTLNowParser':
			siteParser = RTLNowParser.RTLNowParser()
			return siteParser.getShows(url)
		else:
			raise Exception('Unknown Siteparser called!')
	except Exception,e:
		handler = ExceptionHandler.ExceptionHandler(e)
		return handler.getBailOut()

def EpisodesList(parserType = None, url = None, showTitle = None):
	try:
		if parserType == 'RTLNowParser':
			siteParser = RTLNowParser.RTLNowParser()
			return siteParser.getEpisodes(url, showTitle)
		else:
			raise Exception('Unknown Siteparser called!')
	except Exception,e:
		handler = ExceptionHandler.ExceptionHandler(e)
		return handler.getBailOut()

def CreatePrefs():
	INFOMSG = MessageContainer('Select Your Favorit Shows','Hier kann man seine TOP 10 Shows aussuchen. Diese werden dann immer an oberster Stelle om Hauptmenu angezeigt. Vorrausgesetzt, dass Sie "FREE" sind.')
	Prefs.Add(id='loginemail', type='text', default='', label='Login Email')
	Prefs.Add(id='password', type='text', default='', label='Password', option='hidden')
	Prefs.Add(id='cookieallow', type='bool', default=False, label='Allow Netflix Cookie')
#	return False


