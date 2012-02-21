###########################################################################################################
#
# Imports
#
###########################################################################################################
import urllib2_new


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
# Parent Siteparser Class
# Is used as Parent class
#
###########################################################################################################
class SiteParser(object):
	siteRootUrl = None
	pluginPrefix = None

	def getDefaultArt(self):
		return "/video/RTLNetwork/%s/:/resources/%s-art-default.png" % (self.getPluginPrefix(),self.getPluginPrefix())
	def getDefaultThumb(self):
		return "/video/RTLNetwork/%s/:/resources/%s-icon-default.png" % (self.getPluginPrefix(),self.getPluginPrefix())

	def getPluginPrefix(self):
		return self.pluginPrefix

	def getGenres(self):
		Log.Debug('Getting Genres ...')
		oc = ObjectContainer(view_group="List")

		Video_Page = HTML.ElementFromURL(self.siteRootUrl, values=None, headers={}, cacheTime=1)
		# TV Shows Genres ...
		CategoriesContainers = Video_Page.xpath("//div[@id='page']//div[@class='flyout flyout_tvsendungen']//div[@class='flyoutmenu']/ul[3]")[0]
		# News Genres ...
		CategoriesContainers.extend(Video_Page.xpath("//div[@id='page']//div[@class='flyout flyout_news']//div[@class='flyoutmenu']/ul[2]")[0])

		for CategoryContainer in CategoriesContainers:
			CategoryContainer = CategoryContainer.xpath('a')[0]

			oc.add(DirectoryObject(
				key=Callback(ShowsList, url=CategoryContainer.get('href'), parserType=type(self).__name__),
				title=CategoryContainer.text_content(),
				thumb=self.getDefaultThumb(),
				art=self.getDefaultArt()
			))

		return oc

	def getShows(self, url = ''):
		#oc = MediaContainer(viewGroup='Details')
		oc = ObjectContainer(view_group="List")

		Video_Page = HTML.ElementFromURL(self.siteRootUrl + url, values=None, headers={}, cacheTime=None)

		ShowContainers = Video_Page.xpath("//div[@id='page']//div[@class='seriennavi_link']")

		for ShowContainer in ShowContainers:

			# We have to filter:
			# - all elements which are hidden (style="display:none")
			# - all elements wich aren't free
			parent = ShowContainer.getparent()

			# Filter Non-Free Items...
			if not parent.find("div[@class='seriennavi_free']"): continue

			# Filter all elements which aren't on current site... unfortunately javascript takes care of this job
			# so we have to implement the filter-algorithm by ourselves...
			if url != '':
				parentClasses = parent.get('class').split(' ')
				# Filter TV Shows
				if url == '/genre_tv_action.php' and 'seriennavi_genre_2' not in parentClasses: continue
				if url == '/genre_tv_show.php' and 'seriennavi_genre_7' not in parentClasses: continue
				if url == '/genre_tv_soap.php' and 'seriennavi_genre_1' not in parentClasses: continue
				if url == '/genre_tv_crime.php' and 'seriennavi_genre_3' not in parentClasses: continue
				if url == '/genre_tv_comedy.php' and 'seriennavi_genre_5' not in parentClasses: continue

				# Filter News
				if url == '/genre_nm_reportage.php' and 'seriennavi_genre_8' not in parentClasses: continue
				if url == '/genre_nm_news.php' and 'seriennavi_genre_12' not in parentClasses: continue
				if url == '/genre_nm_magazine.php' and 'seriennavi_genre_13' not in parentClasses: continue

			# Add a Line for the Current TV Show to the List
			oc.add(DirectoryObject(
				key = Callback(EpisodesList,
					parserType=type(self).__name__,
					url=ShowContainer.find('a').get('href'),
					showTitle=ShowContainer.text_content().strip()),
				title = ShowContainer.text_content().strip(),
				thumb = self.getDefaultThumb(),
				art   = self.getDefaultArt()
			))

			"""
			oc.add(EpisodeObject(
				key=WebVideoURL(self.siteRootUrl + ShowContainer.find('a').get('href')),
				#url=self.siteRootUrl + showInformation['video_url'],
				rating_key=self.siteRootUrl + showInformation['video_url'],
				title=ShowContainer.text_content().strip(),
				thumb=showInformation['thumb'],
				summary=showInformation['summary'],
				art=showInformation['art']
			))
			"""

			#return MessageContainer("Error!", L(e.message))

		return oc

	def getEpisodes(self, url, showTitle):
		Video_Page = HTML.ElementFromURL(self.siteRootUrl + url, values=None, headers={}, cacheTime=None)

		# Get FREE Episodes... those are located within the first listbg-element
		episodesList = Video_Page.xpath("//div[@id='list_xajax_content']//div[@class='listbg']")[0]
		Log.Debug(episodesList.text_content())

		oc = MediaContainer(viewGroup='Details')
		for episode in episodesList:
			Log.Debug('Appending Episode...')
			oc.Append(WebVideoItem(self.siteRootUrl + episode.find("div/a").get('href'),
				episode.find("div/a").text_content(),
				summary = "Summary",
				thumb = self.getDefaultThumb(),
				art   = self.getDefaultArt()
			))
			#oc.Append(self.getSingleEpisode(episode.find("div/a").get('href')))

		return oc

	def getSingleEpisode(self, url):
		Log.Debug('getSingleEpisode called')
		Video_Page = HTML.ElementFromURL(self.siteRootUrl + url, values=None, headers={}, cacheTime=None)

		#self.getShowEpisodes(url)
		elements = Video_Page.xpath("//script[@type='text/javascript']")

		Log.Debug('Looping Javascript tags ...')
		for scriptTag in elements:
			Log.Debug('Javascript tag found!')
			Log.Debug(type(scriptTag).__name__)
			Log.Debug(scriptTag.text_content())

			if scriptTag.text_content().find('showFlashTeaser_swfobject') != -1:
				detailsUrl = re.search(".*'(http://rtl-now.rtl.de/logic/aufmacher_xml.php?.*)';",scriptTag.text).group(1)

				detailsStructure = XML.ElementFromURL(detailsUrl, values=None, headers={}, cacheTime=1)

				Log.Debug('Appending WebVideoItem')
				return WebVideoItem(
					url     = self.siteRootUrl + detailsStructure.xpath('//link')[0].get('src'),
					thumb   = detailsStructure.xpath('//background09')[0].get('src'),
					title   = re.search(".*(Folge vom ..........).*", detailsStructure.xpath('//info09')[0].text).group(1),
					summary = detailsStructure.xpath('//headline09')[0].text,
					art     = showDetails['thumb']
				)

		Log.Debug('Appending WebVideoItem')
		return WebVideoItem(
			url     = url,
			thumb   = detailsStructure.xpath('//background09')[0].get('src'),
			title   = re.search(".*(Folge vom ..........).*", detailsStructure.xpath('//info09')[0].text).group(1),
			summary = detailsStructure.xpath('//headline09')[0].text,
			art     = showDetails['thumb']
		)

		raise Exception('Could not load Show Information!')
