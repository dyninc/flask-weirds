#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    flask_weirds.weirdserror
    =============================

    Use "import flask.ext.weirds" to import all flask_weirds lib classes.

    This file contains types essential to send messages about errors inside of weirds application.

    Copyright (c) 2012-2013, Dynamic Network Services, Inc. All rights reserved.
    See the included LICENSE file for licensing information.

"""

from objects import errorResponse
import weirdsmodel


class WeirdsException(Exception):
	def __init__(self, error, status):
		self._error = error
		self._status = status

	@property
	def status(self):
		return self._status

	@property
	def error(self):
		return self._error


class WeirdsError(weirdsmodel.WeirdsDataModel):
	def __init__(self, errorCode, title=None, description=None, **kw):
		self.data = errorResponse(errorCode, title, description, **kw)

	def public_data(self):
		return self.data



