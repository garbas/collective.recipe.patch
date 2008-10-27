# -*- coding: utf-8 -*-
"""Recipe for applying patches"""

import os
import zc.recipe.egg


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Scripts(buildout, name, options)
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        """Installer"""

        # 
        egg_path = ??? self.options['egg']

        # 
        patch_content = open(os.path.join(curdir, PATCH_NAME)).read()
        copy = os.path.join(ZODB_FOLDER, PATCH_NAME)
        f = open(copy, 'w')
        try:
            f.write(patch_content)
        finally:
            f.close()

        os.chdir(egg_path)
        os.system('patch -p1 < %s' % patch_path)

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def update(self):
        """Updater"""
        pass
