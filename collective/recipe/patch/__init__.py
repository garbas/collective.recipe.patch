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
        self.options['eggs-directory'] = buildout['buildout']['eggs-directory']
        self.options['develop-eggs-directory'] = buildout['buildout']['develop-eggs-directory']

    def install(self):
        """Installer"""
        
        ws = zc.buildout.easy_install.install(
            [self.options['egg']], self.options['eggs-directory'],
            links           = self.buildout['buildout'].get('find-links', ''),
            index           = self.buildout['buildout'].get('index', ''),
            executable      = self.options['executable'],
            path            = [self.options['develop-eggs-directory']],
            newest          = self.buildout['buildout'].get('newest') == 'true',
            allow_hosts     = self.buildout['buildout'].get('allow-hosts', '*'),
            always_unzip    = 'true', )

        egg_path = ws.require(self.options['egg'])[0].location
        patch_path = os.path.abspath(self.options['patch'])
        os.chdir(egg_path)
        os.system('patch -p0 < %s' % patch_path)

        return egg_path,

    def update(self):
        """Updater"""
        pass
