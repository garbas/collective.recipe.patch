# -*- coding: utf-8 -*-
"""Recipe for applying patches"""
import logging
logger = logging.getLogger('patch')

try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1
import os
from subprocess import Popen, PIPE, STDOUT

import zc.buildout
import zc.recipe.egg

from collective.recipe.patch import patch as patchlib


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.apply_patch = self.binary_or_library(self.options)
        self.patcher = self.egg_or_path(self.options)
        self.patches = self.get_patches(self.options)
        if 'patch' in self.options:
            del self.options['patch']
        if 'patches' in self.options:
            del self.options['patches']
        self.options['hashes'] = str(list(self.calculate_hashes(self.patches)))
        self.options['python'] = self.buildout['buildout']['python']
        self.options['executable'] = self.buildout[self.options['python']]['executable']
        self.options['eggs-directory'] = buildout['buildout']['eggs-directory']
        self.options['develop-eggs-directory'] = buildout['buildout']['develop-eggs-directory']

    def install(self):
        """Installer"""
        return set([self.patcher(patch) for patch in self.patches])

    def update(self):
        """Updater"""
        pass

    @staticmethod
    def get_patches(options):
        """Returns a list of patches."""
        patches = options.get('patches')
        patch = options.get('patch')
        if patch is not None and patches is None:
            patches = patch
        elif patch is not None and patches is not None:
            raise zc.buildout.UserError('Provide only the patches option.')
        return [os.path.realpath(p) for p in patches.split('\n')]

    @staticmethod
    def calculate_hashes(patches):
        """Yields (pathname, SHA1 digest) for each file in `patches`."""
        for patch in patches:
            try:
                yield (patch, sha1(open(patch).read()).hexdigest())
            except IOError:
                raise zc.buildout.UserError('Patch cannot be read: %s' % patch)

    def binary_or_library(self, options):
        """Decides whether to apply patches with an external binary."""
        self.binary = self.options.get('patch-binary')
        if self.binary is None:
            return self.use_patch_library
        else:
            return self.use_patch_binary
        

    def egg_or_path(self, options):
        """Decides whether to apply patches to eggs or paths."""
        egg = options.get('egg')
        path = options.get('path')
        if egg is not None and path is not None:
            raise zc.buildout.UserError('Provide either an egg or path option.')
        elif egg is not None:
            return self.patch_egg
        else:
            return self.patch_path

    def install_egg(self, egg):
        """Installs the specified `egg`."""
        links = self.buildout['buildout'].get('find-links', [])
        if links:
            links = tuple(links.split('\n'))
        ws = zc.buildout.easy_install.install(
            [egg], self.options['develop-eggs-directory'],
            links           = links,
            index           = self.buildout['buildout'].get('index'),
            executable      = self.options['executable'],
            path            = [self.options['eggs-directory']],
            newest          = self.buildout['buildout'].get('newest') == 'true',
            allow_hosts     = self.buildout['buildout'].get('allow-hosts', '*'),
            always_unzip    = 'true', )
        return ws.require(egg)[0].location

    def patch_egg(self, patch):
        """Installs an egg and patches it with `patch`."""
        if getattr(self, 'egg_path', None) is None:
            self.egg_path = self.install_egg(self.options['egg'])
        return self.apply_patch(self.egg_path, patch)

    def patch_path(self, patch):
        """Patches a path with `patch`."""
        return self.apply_patch(self.options['path'], patch)

    def use_patch_binary(self, path, patch):
        """Applies a `patch` to `path` using an external binary."""
        logger.info('reading patch %s' % patch)
        logger.info('in %s...' % path)
        cwd = os.getcwd()
        try:
            os.chdir(path)
            p = Popen([self.binary, '-p0'],
                      stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                      close_fds=True)
            output = p.communicate(open(patch).read())[0]
            [logger.info(line) for line in output.strip().split('\n')]
            if p.returncode != 0:
                raise zc.buildout.UserError('could not apply %s' % patch)
        finally:
            os.chdir(cwd)
        return path

    def use_patch_library(self, path, patch):
        """Applies a `patch` to `path` using patchlib."""
        name = patch
        patch = patchlib.read_patch(name)
        for key in ('source', 'target'):
            patch[key] = [os.path.join(path, p).rstrip('\n')
                          for p in patch[key]]
        logger.info('in %s...' % path)
        if not patchlib.apply_patch(patch):
            raise zc.buildout.UserError('could not apply %s' % name)
        return path
