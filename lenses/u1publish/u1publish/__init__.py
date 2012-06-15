import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('u1publish')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from u1publish import u1publishconfig


class U1publishLens(SingleScopeLens):

    class Meta:
        name = 'u1publish'
        description = 'U1publish Lens'
        search_hint = 'Search for U1 files to publish'
        icon = 'u1publish.svg'
        search_on_blank = True

    # TODO: Add your categories
    no_publish_category = ListViewCategory("No Published", 'help')
    publish_category = ListViewCategory("Published", 'help')

    def search(self, search, results):
        # TODO: Add your search results
        results.append('https://wiki.ubuntu.com/Unity/Lenses/Singlet',
                         'ubuntu-logo',
                         self.example_category,
                         "text/html",
                         'Learn More',
                         'Find out how to write your Unity Lens',
                         'https://wiki.ubuntu.com/Unity/Lenses/Singlet')
        pass

    def obtain_u1_files(self, search):
        pass
