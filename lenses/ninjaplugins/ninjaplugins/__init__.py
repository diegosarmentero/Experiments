import os
import urllib2
import zipfile
try:
    import json
except ImportError:
    import simplejson as json  # lint:ok

from singlet.lens import SingleScopeLens, ListViewCategory


class NinjapluginsLens(SingleScopeLens):

    plugins_folder = os.path.expanduser('~/.ninja_ide/addins/plugins/')
    plugins_descriptor = os.path.join(plugins_folder, "descriptor.json")
    url = 'http://ninja-ide.org/plugins/api/'

    class Meta:
        name = 'ninjaplugins'
        description = 'Ninjaplugins Lens'
        search_hint = 'Search for NINJA-IDE Plugins to install'
        icon = 'ninjaplugins.svg'
        search_on_blank = True

    plugins_category = ListViewCategory("Plugins", 'help')

    def search(self, search, results):
        for name, rate, url in self.search_for_plugins(search):
            results.append(url,
             ('file:///usr/share/unity/lenses/'
              'ninjaplugins/unity-lens-ninjaplugins.svg'),
             self.plugins_category,
             "text/html",
             name,
             'Rate: %s' % rate,
             url)
        pass

    def search_for_plugins(self, search):
        results = []  # [name, url, rate]
        words = search.split()
        if len(words) == 1:
            ninja_query = '%s/%s' % (self.url, search)
            query = json.load(urllib2.urlopen(ninja_query))
        elif len(words) > 1:
            query = json.load(urllib2.urlopen(self.url))
            temp_results = []
            for d in query:
                for word in words:
                    if word in d['tags'] or word in d['name'] or \
                       word in d['description']:
                        temp_results.append(d)
                        break
            query = temp_results
        else:
            query = json.load(urllib2.urlopen(self.url))

        for val in query:
            results.append((val['name'], val['rate'], '-' + val['download']))

        return results

    def handle_uri(self, scope, uri):
        url = uri[1:]
        try:
            if os.path.isdir(self.plugins_folder):
                plugin = self.download_plugin(url)
                self.update_local_plugin_descriptor(plugin, url)
        except Exception, reason:
            print 'plugin could not be installed'
            print reason

    def download_plugin(self, file_):
        '''
        Download a plugin specified by file_
        '''
        #get all the .plugin files in local filesystem
        plugins_installed_before = set(self.__get_all_plugin_descriptors())
        #download the plugin
        fileName = os.path.join(self.plugins_folder, os.path.basename(file_))
        content = urllib2.urlopen(file_)
        f = open(fileName, 'wb')
        f.write(content.read())
        f.close()
        #create the zip
        zipFile = zipfile.ZipFile(fileName, 'r')
        zipFile.extractall(self.plugins_folder)
        zipFile.close()
        #clean up the enviroment
        os.remove(fileName)
        #get the name of the last installed plugin
        plugins_installed_after = set(self.__get_all_plugin_descriptors())
        #using set operations get the difference that is the new plugin
        new_plugin = (plugins_installed_after - plugins_installed_before).pop()
        return new_plugin

    def __get_all_plugin_descriptors(self):
        '''
        Returns all the .plugin files
        '''
        return [pf for pf in os.listdir(self.plugins_folder)
            if pf.endswith('.plugin')]

    def update_local_plugin_descriptor(self, plugin, url):
        '''
        updates the local plugin description
        The description.json file holds the information about the plugins
        downloaded with NINJA-IDE
        This is a way to track the versions of the plugins
        '''
        structure = []
        if os.path.isfile(self.plugins_descriptor):
            read = open(self.plugins_descriptor, 'r')
            structure = json.load(read)
            read.close()
        if os.path.isfile(os.path.join(self.plugins_folder, plugin)):
            read = open(os.path.join(self.plugins_folder, plugin), 'r')
            descriptor = json.load(read)
            read.close()
        #create the plugin data
        plug = {}
        plug['name'] = os.path.basename(plugin)
        plug['version'] = descriptor.get('version', '')
        plug['description'] = descriptor.get('description', '')
        plug['authors'] = descriptor.get('authors', '')
        plug['home'] = url
        plug['download'] = url
        plug['plugin-descriptor'] = plugin
        #append the plugin data
        structure.append(plug)
        descriptor = open(self.plugins_descriptor, 'w')
        json.dump(structure, descriptor, indent=2)
