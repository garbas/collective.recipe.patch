# -*- coding: utf-8 -*-
"""Recipe for applying patches"""

import os
import zc.recipe.egg
import patch as patchlib
from os.path import join


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
        
        patch_path = os.path.abspath(self.options['patch'])
        egg = self.options.get('egg')
        if egg:
            return self.patch_egg(egg, patch_path)
        else:
            path = os.path.abspath(self.options['path'])
            return self.apply_patch(path, patch_path)

    def update(self):
        """Updater"""
        pass

    def patch_egg(self, egg, patch_path):
        """Installer"""
        
        ws = zc.buildout.easy_install.install(
            [egg], self.options['develop-eggs-directory'],
            links           = self.buildout['buildout'].get('find-links', '').split('\n'),
            index           = self.buildout['buildout'].get('index', ''),
            executable      = self.options['executable'],
            path            = [self.options['eggs-directory']],
            newest          = self.buildout['buildout'].get('newest') == 'true',
            allow_hosts     = self.buildout['buildout'].get('allow-hosts', '*'),
            always_unzip    = 'true', )
        egg_path = ws.require(egg)[0].location
        return self.apply_patch(egg_path, patch_path)

    def apply_patch(self, path, patch_path):
        patch_binary = self.options.get('patch-binary', None)
        if patch_binary:
            os.chdir(path)
            os.system('%s -p0 < %s' % (patch_binary, patch_path))
        else:
            patch = patchlib.read_patch(patch_path)
            patch['source'] = [join(path,p).strip() for p in patch['source']]
            patch['target'] = [join(path,p).strip() for p in patch['target']]
            patchlib.apply_patch(patch)

        return [path]
