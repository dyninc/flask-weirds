# -*- coding: utf-8 -*-
"""
    flask_weirds.weirdsapp
    ============================

    Use "import flask.ext.weirds" to import this lib classes.

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


import lxml.etree as etree


mimetypes = (
	('json', 'application/json'),
	('xml',  'text/xml')
)
_mimehash = dict(mimetypes)


class WeirdsResponse(Response):
	"""Special response class to make WEIRDS service
	magic after we have data prepared in python dict"""
	server = "DynWEIRDS 0.1"

	def __init__(self, data, wants='', *args, **kw):
		if hasattr(data, 'public_data'):
			public_data = data.data_expand(data.public_data())
			for uri_block in public_data.get('uris', []):
				uri_block['uri']= current_app.config.get('BASE_URI', "") + uri_block['uri']
		else:
			public_data = data
		
		# What format should we send to client?
		if wants == 'json':
		  serializer = self.serialize_json
		elif wants == 'xml':
		  serializer = self.serialize_xml
		else:
		  accepts = request.accept_mimetypes.best_match(map(lambda x: x[1], mimetypes))
		  if accepts == _mimehash['xml']:
			serializer= self.serialize_xml
		  else:
			## json is default if nothing is detected
			serializer = self.serialize_json
		
		Response.__init__(self, serializer(public_data), *args, **kw)
		self.headers["Server"] = self.server 

	def serialize_json(self, data):
		self.default_mimetype = _mimehash['json']
		return json.dumps(data, indent=4)+"\n"

	def _data_to_xmlnode(self, data, element):
		if isinstance(data, dict):
			for i,v in data.iteritems():
				if isinstance(v, list):
					for x in v:
						self._data_to_xmlnode(x, etree.SubElement(element, i))
				else:
					self._data_to_xmlnode(v, etree.SubElement(element, i))
		elif isinstance(data, list):
			raise RuntimeError("Oops, we can't handle list of lists here....")
		else:
			element.text = str(data)
		return element

	def serialize_xml(self, data):
		self.default_mimetype = _mimehash['xml']
		return etree.tostring( self._data_to_xmlnode(data, etree.Element("weirds")) )


def force_json(f):
	"""This is decorator for function that will return some data, 
	it'll force JSON response class to be used for flask"""
	def func(*args, **kw):
		baseuri = kw.pop
		return WeirdsResponse(*f(*args, **kw), wants='json')
	return func

def force_xml(f):
	"""Same as above, forcing XML response"""
	def func(*args, **kw):
		return WeirdsResponse(*f(*args, **kw), wants='xml')
	return func


class FlaskWeirdsApp(Flask):
	response_class = WeirdsResponse
	
	def route(self, rule, **options):
		"""This replaces standard @app.route decorator to special one that will generate
		three separate flask URL mappings: URI --> function, URI.json --> force_json(function)
		and URI.xml --> force_xml(function)"""
		
		def decorator(f):
			endpoint = f.__name__
			self.add_url_rule(rule, endpoint, f, **options)
			self.add_url_rule(rule + ".json", endpoint + "json", force_json(f), **options)
			self.add_url_rule(rule + ".xml", endpoint + "xml", force_xml(f), **options)
			return f
		return decorator



# You can even overload this decorator in your own app like this:
#
#	def route(route, *args, **kw):
#		def decorator(f):
#			def overload(*args,**kw):
#				## overload action
#				return f(*args, **kw)
#			overload.__name__ = f.__name__
#			parent = flask.ext.weirds.FlaskWeirdsApp.route(app, route, *args, **kw)
#			return parent(overload)
#		return decorator
#
#
