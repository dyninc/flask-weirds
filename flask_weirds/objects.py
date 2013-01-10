#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
   flask_weirds.objects
   
   Includes common structures that WEIRDS uses.

   See https ://datatracker.ietf.org/doc/draft-ietf-weirds-json-response/ for 
   more information.

   :copyright: (c) 2012 Dyn Inc, <hello@dyn.com>
   :license: BSD, see attached file LICENSE for more info

"""


def _convertAndAdd(workDict, nonArrayKeys, whatToAdd):
	"""Private func to help to functions below."""

	for (k, v) in workDict.items():
		if v is None:
			del workDict[k]
		elif isinstance(v, (list, tuple)):
			# lists get cleaned for "None" and "" values
			clean = []
			for one in v:
				if one is None or (isinstance(one, basestring) and one == ""):
					continue
				clean.append(one)
			if len(clean) == 0:
				del workDict[k]
			elif len(clean) < len(v):
				workDict[k] = clean
		elif nonArrayKeys is not None and k not in nonArrayKeys:
			# only convert those elements that not protected
			# None means "all protected"
			workDict[k] = [v]
	if whatToAdd is not None:
		for (k, v) in whatToAdd.iteritems():
			if v is not None:
				workDict[k] = v

	return workDict


def rdapConformance(*args):
	"""The first data structure is named "rdapConformance" and is simply an
	array of strings, each providing a hint as to the specifications used
	in the construction of the response.

	:param args: the list of strings to include to rdapConformance array
	"""

	return {'rdapConformance': args}


def notice(title, description=None, links=None):
	"""The second data structure is named "notices" and is an array of
	objects.  Each object contains a "title" string representing the
	title of the notice object, an array of strings named "description"
	for the purposes of conveying any descriptive text about the notice,
	and an optional "links" object as described in Section 6.

	This function generates one notice that could be joined into array.

	:param title: string to use as a title
	:param description: string or list of strings for a description
	:param links: dicts of info to use as "links" (all fields are used).

	Note: function will not fail but will produce unexpected results if 
	incorrect arguments are given.
	"""

	ret = {'title': title, 'description': description, 'links': links}
	return _convertAndAdd(ret, ['title'], None)


def link(value, rel=None, tp=None, href='<<<same as value>>>'):
	"""At some point I got lazy and decided to write common structure
	to generate links, here is generator for it.

	:param value: value field of link object
	:param rel: rel field, no default value there
	:param type: type field
	:param href: href field, defaults to "same as value"
	"""

	if href is not None and href == '<<<same as value>>>':
		href = value
	ret = {
		'value': value,
		'rel': rel,
		'type': tp,
		'href': href,
		}
	return _convertAndAdd(ret, None, None)


def entity(
	handle,
	entityNames,
	status=None,
	roles=None,
	postalAddress=None,
	emails=None,
	phones=None,
	remarks=None,
	links=None,
	**kw
	):
	"""This object class represents the information of organizations,
	corporations, governments, non-profits, clubs, individual persons, and
	informal groups of people.

	:param handle: name of the entity
	:param entityNames: array of strings signifying possible name of the entity
	:param roles: relationship in the parent object to the entity
	:param status: strings describing entity status in registry
	:param postalAddress: strings representing mailing address
	:param emails: list of email addresses for the entity
	:param phones: object containing telephone information, with descriptive keys
	:param remarks: list of strings commenting the entity
	:param links: links for the entity
	:param kw: could contain anything else to add to the entity object
	
	* values that are ought to be lists will be auto-built as list of one
	  element if string was provided.
	* phones will be built from single string as {"office":phones} object.
	* links would not be constructed from plain string.
	"""

	if isinstance(phones, basestring):
		phones = {'office': phones}

	ret = {
		'handle': handle,
		'entityNames': entityNames,
		'status': status,
		'roles': roles,
		'postalAddress': postalAddress,
		'emails': emails,
		'phones': phones,
		'remarks': remarks,
		'links': links,
		}
	return _convertAndAdd(ret, ['handle', 'phones'], kw)


def nameserver(
	handle,
	name,
	status=None,
	ipAddresses=None,
	remarks=None,
	links=None,
	**kw
	):
	"""The nameserver object class is used by both RIRs and DNRs.

	:param handle: registry handle of the nameserver
	:param name: nameserver hostname
	:param status: list of strings signifying status of nameserver in the registry
	:param ipAddresses: list of strings representing ipv4 and ipv6 addresses
	:param remarks: nameserver object string remarks
	:param links: links for the nameserver
	:param kw: all other values that should be included 
	"""

	ret = {
		'handle': handle,
		'name': name,
		'status': status,
		'ipAddresses': ipAddresses,
		'remarks': remarks,
		'links': links,
		}
	return _convertAndAdd(ret, ['handle', 'name'], kw)


def delegationKey(algorithm, digest, digestType, keyTag):
	"""The delegationKey object is set of properties describing DNSSEC records.

	:param algorithm: int algorithm field of a DNS DS record
	:param digest: string digest of the DS record
	:param digestType: int digest type field from DS
	:param keyTag: int keytag value from the DS
	"""

	return {
		'algorithm': algorithm,
		'digest': digest,
		'digestType': digestType,
		'keyTag': keyTag,
		}


def domain(
	handle,
	name,
	variants=None,
	status=None,
	nameservers=None,
	entities=None,
	delegationKeys=None,
	remarks=None,
	links=None,
	**kw
	):
	"""The domain object class represents a DNS name and point of
   delegation.  For RIRs these delegation points are in the reverse DNS
   tree, whereas for DNRs these delegation points are in the forward DNS
   tree.

   :param handle: ID of the domain object in the registry
   :param name: domain name
   :param variants: variant object array
   :param status:	list of strings signifying domain status 
   :param nameservers: list of nameserver objects 
   :param entities: list of entity objects
   :param delegationKeys: list of delegation keys objects
   :param remarks: list of comment strings 
   :param links: list of links objects for this domain
   :param kw: all additional string fields that we might need  
	"""

	ret = {
		'handle': handle,
		'name': name,
		'variants': variants,
		'status': status,
		'nameServers': nameservers,
		'entities': entities,
		'delegationKeys': delegationKeys,
		'remarks': remarks,
		'links': links,
		}
	return _convertAndAdd(ret, ['handle', 'name'], kw)


def ip(
	handle,
	startAddress,
	endAddress,
	name=None,
	description=None,
	remarks=None,
	links=None,
	entities=None,
	**kw
	):
	"""The IP Network object class models IP network registrations found in RIRs and is the 
	expected response for the /ip query.

	:param handle: ID of the IP object in the registry
	:param startAddress: start IP address (ipv4 or v6)
	:param endAddress: end IP address for this network
	:param name: name of the network
	:param description: list of description strings for this network 
	:param remarks: list of text remarks
	:param links: list of links for this IP object
	:param entities: list of associated entities
	:param kw: all other string fields
	"""

	ret = {
		'handle': handle,
		'startAddress': startAddress,
		'endAddress': endAddress,
		'name': name,
		'description': description,
		'remarks': remarks,
		'links': links,
		'entities': entities,
		}
	return _convertAndAdd(ret, ['handle', 'startAddress', 'endAddress', 'name'], kw)


def autnum(
	handle,
	startAutnum,
	endAutnum,
	name=None,
	description=None,
	remarks=None,
	links=None,
	entities=None,
	**kw
	):
	"""The Autonomous System Number (autnum) object class models 
	Autonomous System Number registrations found in RIRs and represents the 
	expected response to an /autnum query.

	:param handle: ID of the autonomous system object in the registry
	:param startAutnum: start AS number in the block
	:param endAutnum: end AS number
	:param name: name of the AS
	:param description: list of description strings for this AS
	:param remarks: list of text remarks
	:param links: list of links for this AS object
	:param entities: list of entities associated with the AS
	:param kw: all other string fields
	"""

	ret = {
		'handle': handle,
		'startAutnum': startAutnum,
		'endAutnum': endAutnum,
		'name': name,
		'description': description,
		'remarks': remarks,
		'links': links,
		'entities': entities,
		}
	return _convertAndAdd(ret, ['handle', 'startAutnum', 'endAutnum', 'name'], kw)


def errorResponse(errorCode, title=None, description=None, **kw):
	"""The basic structure of that response is an object class containing an error code number.
	:param errorCode: integer number signifying an error condition
	:param title: string value describing an error  
	:param description: freeform error comment strings
	:param kw: other free-form fields
	"""

	ret = {'errorCode': errorCode, 'title': title, 'description': description}
	return _convertAndAdd(ret, ['errorCode', 'title'], kw)
