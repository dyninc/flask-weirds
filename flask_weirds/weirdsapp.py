#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
		flask_weirds.weirdsapp
		============================

		Use "import flask.ext.weirds" to import this lib class.

		This library overrides Flask app class to achieve magic of XML/JSON answer without
		writing additional logic for that. It's recommended to use data model from weirdsmodel
		module.

		Copyright (c) 2012-2013, Dynamic Network Services, Inc. All rights reserved.
		See the included LICENSE file for licensing information.

"""

import flask
from weirdsmodel import WeirdsDataModel
from weirdserror import WeirdsException, WeirdsError
from flask import current_app
import json

MIME_TYPE = 'application/rdap'
SERVER_VERSION = '1.1.0'

ERR_PATH_NOT_FOUND = (WeirdsError(0xff00, 'Bad Request', 'Invalid object type or path in your request.'), '400 Bad Request')
ERR_OBJECT_NOT_FOUND = (WeirdsError(0xff01, 'Not Found', 'Requested object was not found in our database.'), '404 Not Found')
ERR_OUTAGE = (WeirdsError(0xff01, 'Internal Error', 'Our systems are not functioning properly at the moment.'), '500 Internal Server Error')
ERR_AUTHINVALID = (WeirdsError(0xff03, 'Auth Invalid', 'Please use correct username and password to see authenticated request response.'), '401 Auth Required')


class WeirdsResponse(flask.Response):
	"""Special response class to make WEIRDS service
	magic after we have data prepared in python dict"""

	server = 'DynWEIRDS ' + SERVER_VERSION

	def __init__(self, data, *args, **kw):
		if len(args) == 0:
			args = ['200 OK']
		else:
			args = list(args)
		try:
			raw_public_data = data.public_data()
			if raw_public_data is None:
				raise WeirdsException(*ERR_OBJECT_NOT_FOUND)

			public_data = data.data_expand(raw_public_data)
			for uri_block in public_data.get('links', []):
				for hrefkey in ['value', 'href']:
					if isinstance(uri_block[hrefkey], basestring) and '//' not in uri_block[hrefkey]:
						uri_block[hrefkey] = current_app.config.get('BASE_URI', '') + uri_block[hrefkey]
		except WeirdsException, e:
			public_data = e.error.data
			args[0] = e.status

		self.default_mimetype = MIME_TYPE
		flask.Response.__init__(self, json.dumps(public_data, indent=4) + '\n', *args, **kw)
		self.headers['Server'] = self.server


class WeirdsApp(flask.Flask):
	"""This is Flask app that knows what to do if view function returns WeirdsDataModel.
	It will generate WeirdsResponse for those cases, hiding as normal App otherwise.
	"""

	def __init__(self, *args, **kw):
		flask.Flask.__init__(self, *args, **kw)
		self.register_error_handler(404, lambda x: ERR_PATH_NOT_FOUND)
		self.register_error_handler(401, lambda x: ERR_AUTHINVALID)
		self.register_error_handler(500, lambda x: ERR_OUTAGE)

	def make_response(self, rv):
		if isinstance(rv, WeirdsDataModel):
			return WeirdsResponse(rv)
		elif isinstance(rv, (list, tuple)) and len(rv) > 0 and isinstance(rv[0], WeirdsDataModel):
			return WeirdsResponse(*rv)
		else:
			return flask.Flask.make_response(self, rv)


