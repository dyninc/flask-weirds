#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    flask_weirds.weirdsmodel
    =============================

    Use "import flask.ext.weirds" to import this lib classes.

    Base data model classes that needs to be used (extended) for flask-weirds application code.

    Copyright (c) 2012, Dynamic Network Services, Inc. All rights reserved.
    See the included LICENSE file for licensing information.

"""

from objects import errorResponse

class WeirdsDataModel(object):

	"""This class defines an Interface to return data from weirdsapp routes"""

	def public_data(self):
		return {}

	def push_expand(self, expanditem):
		expandlist = getattr(self, '_expandlist', [])
		try:
			newsub = getattr(self, 'expand_{0}'.format(expanditem))
		except:
			raise WeirdsDataError('Cannot apply expand_{0} to object of this type'.format(expanditem))
		expandlist.append(newsub)
		self._expandlist = expandlist

	def data_expand(self, data):
		expandlist = getattr(self, '_expandlist', [])
		for sub in expandlist:
			sub(data)
		return data


class WeirdsError(WeirdsDataModel):
	def __init__(self, errorCode, title=None, description=None, **kw):
		self.data = errorResponse(errorCode, title, description, **kw)

	def public_data(self):
		return self.data



