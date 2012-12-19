#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Flask-Weirds
    ====================

    Flask extension to create WEIRDS applications.

    Typical use similar to the following sudo-code:

        class ObjectModel(flask.ext.weirds.WeirdsDataModel):
            def __init__(self, name):
                self.name = find_magic_object(name)
            
            def public_data(self):
                return { 'name' : self.name}
        
        app = flask.ext.weirds.FlaskWeirdsApp(__name__)
        
        @app.route('/object/<name>')
        def object(name):
          return ObjectModel(name),

    You may find similar bits of code in example, provided with this package,
    weirdsexample.py.
"""

from flask_weirds.weirdsapp import SERVER_VERSION
from setuptools import setup
setup(
	name='Flask-Weirds',
	version=SERVER_VERSION,
	license='BSD',
	author='Dyn Inc',
	author_email='hello@dyn.com',
	description='Flask extension to create WEIRDS applications.',
	long_description=__doc__,
	packages=['flask_weirds'],
	include_package_data=True,
	zip_safe=False,
	platforms='any',
	install_requires=['Flask'],
	classifiers=[
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: Software Development :: Libraries :: Python Modules',
		],
	)
