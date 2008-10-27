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

Our demo package which will patch.

    >>> mkdir(sample_buildout, 'demo')
    >>> write(sample_buildout, 'demo', 'README.txt', " ")
    >>> write(sample_buildout, 'demo', 'demo.py',
    ... """# demo egg 
    ... """)
    >>> write(sample_buildout, 'demo', 'setup.py',
    ... """
    ... from setuptools import setup
    ...
    ... setup(
    ...     name = "demo",
    ...     version='1.0',
    ...     py_modules=['demo']
    ...     )
    ... """)
    >>> print system(buildout+' setup demo bdist_egg'), # doctest: +ELLIPSIS
    Running setup script 'demo/setup.py'.
    ...


Create out patch.

    >>> write(sample_buildout, 'demo.patch',
    ... """diff --git demo.py demo.py
    ... --- demo.py
    ... +++ demo.py
    ... @@ -1 +1,2 @@
    ...  # demo egg
    ... +# patching
    ... """)


Let now write out buildout.cfg to patch our demo package

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = demo-eggs demo-patch
    ... index = %(dist)s
    ...
    ... [demo-eggs]
    ... recipe = zc.recipe.egg
    ... eggs = demo
    ...
    ... [demo-patch]
    ... recipe = collective.recipe.patch
    ... egg = %(egg)s
    ... patch = %(patch)s
    ... """ % { 'egg'   : 'demo==1.0', 
    ...         'patch' : 'demo.patch',
    ...         'dist'  : join('demo', 'dist'), })



Running the buildout gives us::

    >>> print 'start', system(buildout) 
    start Not found: demo/dist/zc.buildout/
    ...
    >>> ls(sample_buildout, 'eggs-patched')
    d  demo-1.0-py2.4.egg
    >>> cat(sample_buildout, 'demo', 'demo.py')
    # demo egg 
    >>> cat(sample_buildout, 'eggs-patched', 'demo-1.0-py2.4.egg', 'demo.py')
    # demo egg 
    # patching

