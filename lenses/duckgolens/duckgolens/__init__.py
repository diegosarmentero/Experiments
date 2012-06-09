import logging
import optparse

import duckduckgo

import gettext
from gettext import gettext as _
gettext.textdomain('duckgolens')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from duckgolens import duckgolensconfig


class DuckgolensLens(SingleScopeLens):

    class Meta:
        name = 'duckgolens'
        description = 'Duckgolens Lens'
        search_hint = 'Search DuckDuckGo'
        icon = 'duckgolens.svg'
        search_on_blank = True

    # TODO: Add your categories
    search_category = ListViewCategory("Results", 'help')

    def search(self, search, results):
        # TODO: Add your search results
        for text, url in self.duckduckgo_query(search):
            results.append(url,
             'http://upload.wikimedia.org/wikipedia/en/thumb/2/24/Duck_Duck_Go.svg/200px-Duck_Duck_Go.svg.png',
             self.search_category,
             "text/html",
             text,
             'DuckDuckGo Result',
             url)
        pass

    def duckduckgo_query(self, search):
        print search
        results = []  # (Text, Link)
        if not search:
            return results
        print '\n'
        print 'searchingggggggggggg'
        print search
        query = duckduckgo.query(search)
        if query.answer is not None:
            results.append((query.answer.text, 'http://duckduckgo.com/'))
            return results
        for result in query.results:
            results.append((result.text, result.url))
        for related in query.related:
            text = 'Related: %s' % related.text
            results.append((text, related.url))

        return results
