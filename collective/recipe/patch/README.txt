Supported options
=================

The recipe supports the following options:

egg
    Define which egg should be patched. You can also pin to version.
    example: some.egg<=1.1.1

patch
    Path to patch file. 
    example: patches/my_very_sprecial.patch

Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = demo-patch
    ...
    ... [demo-patch]
    ... recipe = collective.recipe.patch
    ... egg = %(egg)s
    ... patch = %(patch)s
    ... """ % { 'egg' : 'demo_egg', 'patch' : 'patches/demo_egg.patch'})

Running the buildout gives us::

    >>> print 'start', system(buildout) 
    start...
    Installing patch.
    Unused options for test1: 'option2' 'option1'.
    <BLANKLINE>


