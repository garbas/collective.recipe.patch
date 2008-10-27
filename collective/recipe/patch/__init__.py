# -*- coding: utf-8 -*-
"""Recipe for applying patches"""

import os
import zc.recipe.egg


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(buildout, name, options)

        self.options['python'] = self.buildout['buildout']['python']
        self.options['executable'] = self.buildout[self.options['python']]['executable']
        self.options['eggs-directory'] = os.path.join(buildout['buildout']['directory'], 'eggs-patched')
        self.options['develop-eggs-directory'] = os.path.join(buildout['buildout']['develop-eggs-directory'], 'develop-eggs-patched')

    def install(self):
        """Installer"""
        print 'TESTING'
        # install patched egg into patched directory
        if self.buildout['buildout'].get('offline') == 'true':
            ws = zc.buildout.easy_install.working_set(
                [self.options['egg']], self.options['executable'],
                [self.options['develop-eggs-directory'], self.options['eggs-directory']] )
        else:
            ws = zc.buildout.easy_install.install(
                [self.options['egg']], self.options['eggs-directory'],
                links           = self.buildout['buildout'].get('find-links', ''),
                index           = self.buildout['buildout'].get('index', ''),
                executable      = self.options['executable'],
                path            = [self.options['develop-eggs-directory']],
                newest          = self.buildout['buildout'].get('newest') == 'true',
                allow_hosts     = self.buildout['buildout'].get('allow-hosts', '*'),
                always_unzip    = 'true', )


        egg_path = ws.by_key.values()[0].location
        patch_path = os.path.abspath(self.options['patch'])
        print open(egg_path+'/demo.py').read()
        os.chdir(egg_path)
        os.system('patch -p0 < %s' % patch_path)
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        print 'PATCHED'
        print open(egg_path+'/demo.py').read()
        return egg_path,

    def update(self):
        """Updater"""
        pass
