#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    weirdsexample
    ================

    WSGI application to provide basic abstract-data-source WEIRDS service and
    demonstrate Flask-Weirds extension

    :copyright: (c) 2012 Alex Sergeyev <hello@dyn.com>, Dyn Inc <http://dyn.com/>. All Rights Reserved
    
"""

import flask
import flask.ext.weirds as weirds
import sys

# Error messages encoded as tuple {'error':'error info', ...}, "HTTP response code"

ERR_PATH_NOT_FOUND = ( weirds.WeirdsError(400, "Bad Request", "Invalid object type or path in your request."), '400 Bad Request' )
ERR_OBJECT_NOT_FOUND = ( weirds.WeirdsError(404, "Not Found", "Requested object was not found in our database."), '404 Not Found' )
ERR_OUTAGE = ( weirds.WeirdsError(500, "Internal Error", "Our systems are not functioning properly at the moment."), '500 Internal Server Error' )

# see module for details about overloads to Flask in that module and tricks we employ

app = weirds.WeirdsApp(__name__)
app.config.update(BASE_URI='http://weirdshost.example.org')


## This is fake Data Model, do not use it in your application:

class DomainFakeModel(weirds.WeirdsDataModel):

	def __init__(self, name):
		self.name = name.lower()

	def public_data(self):
		return weirds.domain(None, self.name)


def find_fake_domain(domainname):
	try:
		(name, rest) = domainname.split('.', 1)
		assert name == 'example' and rest in ('org', 'com', 'net', 'edu')
	except:
		return None

	return DomainFakeModel(domainname)


##  See flask-sqlalchemy if you'd need to have DB access here:
##     db = SQLAlchemy(app)
## and define your modules in external module or here,
##     class SomeDataModel(db.Model):
##         def public_data(self):
##             return { "key" : "value" }
##
## then your "find_somedata" would use:
##     SomeDataModel.query.filter_by(name = domainname).first()
##
## and so on...

@app.errorhandler(404)
def notfound(dummy_e):
	return ERR_PATH_NOT_FOUND


@app.errorhandler(500)
def crash(dummy_e):
	return ERR_OUTAGE


## WARNING
#
#  Flask "route" subs below should always return a tuple of DICT, HTTP_ANSWER, and then some.
#  In our case we're returning DICT of data that should be converted to JSON/XML but to force
#  list context we must not omit trailing comma in those "return" statements that succeed
#

@app.route('/fakedomain/<domainname>')
def fakedomain(domainname):
	domain = find_fake_domain(domainname)
	if domain is None:
		return ERR_OBJECT_NOT_FOUND
	return domain

if __name__ == '__main__':

	# This is startup procedure when we run this code from command line.
	# We can also use "uwsgi -w weirdsexample --callable app --http 0.0.0.0:5000"
	# to achieve similar result and employ advanced HTTP engine

	print 'Running the app, you should be able to query http://hostname:5000/fakedomain/example.org'
	print '...'
	print 'Try also .net .edu .info and other domains :)'
	app.run(host='0.0.0.0', port=5000, debug='--debug' in sys.argv)

	# Notes:
	# 1. see flask doc about "debug=True" mode
	# 2. you can also use fcgi or uwsgi runners, keyword "werkzeug" (that's
	# lib that flask uses) will help you google for instructions
	#   (run uwsgi --help to change command line above to uwsgi or fastcgi
	# if you like uwsgi as much as I do)
	# 3. I like uwsgi that's why I don't put host/port to config so far...
	# I'll check if I can address this in better way later (I think I should)
	#
	# You need nginx or other frontend to react to Accept: text/xml and use .xml by default
