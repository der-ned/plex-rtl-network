###########################################################################################################
#
# Imports
#
###########################################################################################################
import SiteParser


###########################################################################################################
#
# Dummies for Handlers... unfortunately... we need them
#
###########################################################################################################
def ShowsList(parserType = None, url = None):
	return None
def EpisodesList(parserType = None, url = None, showTitle = None):
	return None

###########################################################################################################
#
# RTLNow Parser class
#
###########################################################################################################
class RTLNowParser(SiteParser.SiteParser):
	siteRootUrl = "http://rtl-now.rtl.de"

	pluginPrefix = 'rtlnow'

	mainArt = "/video/RTLNetwork/RTLNow/:/resources/%s" % ("rtlnow-art-default.png")
	mainThumb = "/video/RTLNetwork/RTLNow/:/resources/%s" % ("rtlnow-icon-default.png")

	def getSiteName(self): return 'RTL Now - RTL Television'
