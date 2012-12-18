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

from flask import Response, Flask, request, current_app

try:
	import json
except ImportError:
	import simplejson as json


MIME_TYPE = "application/rdap"

class WeirdsResponse(Response):
	"""Special response class to make WEIRDS service
	magic after we have data prepared in python dict"""

	server = 'DynWEIRDS 0.2'

	def __init__(self, data, *args, **kw):
		if hasattr(data, 'public_data'):
			public_data = data.data_expand(data.public_data())
			for uri_block in public_data.get('links', []):
				for hrefkey in ['value', 'href',]:
					if isinstance(uri_block[hrefkey], basestring)  and  "//" not in uri_block[hrefkey]:
						uri_block[hrefkey] = current_app.config.get('BASE_URI', '') + uri_block[hrefkey]
		else:
			public_data = data

		Response.__init__(self, self.serializer(public_data), *args, **kw)
		self.headers['Server'] = self.server

	def serializer(self, data):
		self.default_mimetype =  MIME_TYPE
		return json.dumps(data, indent=4) + '\n'


class FlaskWeirdsApp(Flask):
	def make_response(self, rv):
		return WeirdsResponse(*rv)
