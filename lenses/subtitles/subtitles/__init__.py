import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('subtitles')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from subtitles import subtitlesconfig

import urllib2
from BeautifulSoup import BeautifulSoup

class SubtitlesLens(SingleScopeLens):

    class Meta:
        name = 'subtitles'
        description = 'Subtitles Lens'
        search_hint = 'Search Subtitles'
        icon = 'subtitles.svg'
        search_on_blank=True

    # TODO: Add your categories
    subtitles_category = IconViewCategory("Subtitles", 'help')

    subtitles = 'http://www.subtitulos.es/'
    shows = {}

    def search(self, search, results):
        for text, url in self.subtitles_query(search):
            results.append(url,
             'http://a.fsdn.com/con/icons/gn/gnome-subtitles@sf.net/gnome-subtitles.png',
             self.subtitles_category,
             "text/html",
             text,
             'Subtitles.es',
             url)
        pass

    def subtitles_query(self, search):
        results = []
        if not search:
            return results
        print 'Searching for:', search
        if not self.shows:
            url = self.subtitles + 'series'
            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page)
            tds = soup.findAll('td')
            for td in tds:
                a = td.find('a')
                if a is None:
                    continue
                url = a.attrs[0][1]
                if url.startswith('/'):
                    url = url[1:]
                url = self.subtitles + url
                self.shows[a.text.lower()] = url

        search = unicode(search)
        selected = [show for show in self.shows if show.startswith(search)]
        for name in selected:
            results.append((name, self.shows[name]))

        return results
