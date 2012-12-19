#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
		flask_weirds.weirdsapp
		============================

		Use "import flask.ext.weirds" to import this lib class.

		This library overrides Flask app class to achieve magic of XML/JSON answer without
		writing additional logic for that. It's recommended to use data model from weirdsmodel
		module.

		Copyright (c) 2012, Dynamic Network Services, Inc. All rights reserved.
		See the included LICENSE file for licensing information.

"""

import flask
from weirdsmodel import WeirdsDataModel

try:
	import json
except ImportError:
	import simplejson as json

MIME_TYPE = 'application/rdap'


class WeirdsResponse(flask.Response):

	"""Special response class to make WEIRDS service
	magic after we have data prepared in python dict"""

	server = 'DynWEIRDS 0.2'

	def __init__(self, data, *args, **kw):
		public_data = data.data_expand(data.public_data())
		for uri_block in public_data.get('links', []):
			for hrefkey in ['value', 'href']:
				if isinstance(uri_block[hrefkey], basestring) and '//' not in uri_block[hrefkey]:
					uri_block[hrefkey] = current_app.config.get('BASE_URI', '') + uri_block[hrefkey]

		self.default_mimetype = MIME_TYPE
		flask.Response.__init__(self, json.dumps(public_data, indent=4) + '\n', *args, **kw)
		self.headers['Server'] = self.server


class WeirdsApp(flask.Flask):

	"""This is Flask app that knows what to do if view function returns WeirdsDataModel.
	It will generate WeirdsResponse for those cases, hiding as normal App otherwise.
	"""

	response_class = WeirdsResponse

	def make_response(self, rv):
		if isinstance(rv, WeirdsDataModel):
			return self.response_class(rv)
		elif isinstance(rv, (list, tuple)) and len(rv) > 0 and isinstance(rv[0], WeirdsDataModel):
			return self.response_class(*rv)
		else:
			return flask.Flask.make_response(self, rv)
