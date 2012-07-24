# -*- coding: utf-8 -*-
"""
    flask_weirds.weirdsmodel
    =============================

    Use "import flask.ext.weirds" to import this lib classes.

    Base data model classes that needs to be used (extended) for flask-weirds application code.

    Copyright (c) 2012, Dynamic Network Services, Inc. All rights reserved.
    See the included LICENSE file for licensing information.

"""

class WeirdsDataError(RuntimeError):
	"""Base exception class to raise errors in case if data operations could not be completed"""
	pass

class WeirdsDataModel(object):
	"""This class defines an Interface to return data from weirdsapp routes"""
	def public_data(self):
		return {}
	
	def expand_data(self):
		raise WeirdsDataError("This is abstract method to prevent basic WeirdsDataModel to be used as WeirdsExpandMixin")


class WeirdsExpandMixin:
	"""This mixin is used to modify normal data objects with additional data.
	Usage:
	
	@app.route("/somepath/<objectid>")
	def somepath_handler(objectid):
		weirds_data_object = find_data_object(objectid)
		if flask.request.authorization.username == "superuser":
			user.push_expand("billing_info")
		return weirds_data_object,
	
	In this case process will be completed as is and in the end, flask-app will generate
	response from data, constructed like this:
		struct_to_print = weirds_data_object.data_expand(weirds_data_object.public_data())
	which will call internally method
		weirds_data_object.expand_billing_info(public_data_submitted)
	
	This design decision is made to abstract "permissioning" from actual "data delivery".
	"""
	def push_expand(self, expanditem):
		expandlist = getattr(self, '_expandlist', [])
		try:
			newsub = getattr(self, 'expand_{0}'.format(expanditem))
		except:
			raise WeirdsDataError("Cannot apply expand_{0} to object of this type".format(expanditem))
		expandlist.append(newsub)
		self._expandlist = expandlist
	
	def data_expand(self, data):
		expandlist = getattr(self, '_expandlist', [])
		for sub in expandlist:
			sub(data)
		return data


