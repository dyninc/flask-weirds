# -*- coding: utf-8 -*-

import objects
import unittest

try:
	import json
except ImportError:
	import simplejson as json


class WeirdsTestCase(unittest.TestCase):

	def assertJSON(self, src, dst):
		if isinstance(src, basestring):
			src = json.loads(src)
		if isinstance(dst, basestring):
			dst = json.loads(dst)
		src = json.dumps(src, sort_keys=True)
		dst = json.dumps(dst, sort_keys=True)
		if src != dst:
			msg = "Results are not same:\n" + src + "\n" + dst + "\n"
			for i in range(1,len(src)):
				if src[0:i] != dst[0:i]:
					msg += " "*(i-1) + "^^\n"
					break
			self.fail(msg)



class RdapConformanceTest(WeirdsTestCase):

	def test_rdapConformanceOneElement(self):
		result = objects.rdapConformance('rdap_level_0')
		self.assertJSON(result, {'rdapConformance': ['rdap_level_0']})

	def test_rdapConformanceTwoElements(self):
		result = objects.rdapConformance('rdap_level_0', 'lunarNic_level_0')
		self.assertJSON(result, {'rdapConformance': ['rdap_level_0', 'lunarNic_level_0']})


class NoticesTest(WeirdsTestCase):

	def test_nominalNotice(self):
		reslt = objects.notice('Terms of Use', ['This service is subject to The Registry of the Moons', 'terms of service.'], {
			'value': 'http://example.net/entity/XXXX',
			'rel': 'alternate',
			'type': 'text/html',
			'href': 'http://www.example.com/terms_of_use.html',
			})
		self.assertJSON(reslt,
                  """{
						"title" : "Terms of Use",
						"description" : [
							"This service is subject to The Registry of the Moons",
							"terms of service."
						],
						"links" : [ {
								"value" : "http://example.net/entity/XXXX",
								"rel" : "alternate",
								"type" : "text/html",
								"href" : "http://www.example.com/terms_of_use.html"
							}]
						}""")


class EntityTest(WeirdsTestCase):

	def test_dnrEntity(self):
		answer = \
   """{
			"handle" : "XXXX",
			"entityNames": [ "Joe Bob, Inc.", "Bobby Joe Shopping" ],
			"status" : [ "validated", "locked" ],
			"postalAddress" : [
				"123 Maple Ave",
				"Suite 90001",
				"Vancouver",
				"BC",
				"12393"
			],
			"emails" : [ "joe@bob.com", "bob@joe.com" ],
			"phones" : {
				"office" : [ "1-958-555-4321", "1-958-555-4322" ],
				"fax" : [ "1-958-555-4323" ],
				"mobile" : [ "1-958-555-4324" ]
			},
			"remarks" : [
				"she sells seas shells",
				"down by the seashore"
			],
			"links" : [ {
				"value" : "http://example.com/entity/XXXX",
				"rel" : "self",
				"href" : "http://example.com/entity/XXXX"
			} ],
			"port43" : "whois.example.net",
			"registrationDate" : "1990-12-31T23:59:60Z",
			"registrationBy" : "ABC123",
			"lastChangedDate" : "1990-12-31T23:59:60Z",
			"lastChangedBy" : "ABC123",
			"sponsoredBy" : "SponsorXYZ",
			"resoldBy" : "ResellerPDQ"
			}"""

		reslt = objects.entity(  # roles
			'XXXX',
			['Joe Bob, Inc.', 'Bobby Joe Shopping'],
			['validated', 'locked'],
			None,
			['123 Maple Ave', 'Suite 90001', 'Vancouver', 'BC', '12393'],
			['joe@bob.com', 'bob@joe.com'],
			{'office': ['1-958-555-4321', '1-958-555-4322'], 'fax': ['1-958-555-4323'], 'mobile': ['1-958-555-4324']},
			['she sells seas shells', 'down by the seashore'],
			{'value': 'http://example.com/entity/XXXX', 'rel': 'self', 'href': 'http://example.com/entity/XXXX'},
			port43='whois.example.net',
			registrationDate='1990-12-31T23:59:60Z',
			registrationBy='ABC123',
			lastChangedDate='1990-12-31T23:59:60Z',
			lastChangedBy='ABC123',
			sponsoredBy='SponsorXYZ',
			resoldBy='ResellerPDQ',
			)
		self.assertJSON(reslt, answer)

	def test_rirEntity(self):
		answer = \
   """{
			"handle" : "XXXX",
			"entityNames": [ "Joe Bob, Inc.", "Bobby Joe Shopping" ],
			"roles" : [ "registrant" ],
			"postalAddress" : 
			[
				"123 Maple Ave",
				"Suite 90001",
				"Vancouver",
				"BC",
				"12393"
			],
			"emails" : [ "joe@bob.com", "bob@joe.com" ],
			"phones" : 
			{
				"office" : [ "1-958-555-4321", "1-958-555-4322" ],
				"fax" : [ "1-958-555-4323" ],
				"mobile" : [ "1-958-555-4324" ]  
			},
			"remarks" : 
			[
				"she sells seas shells",
				"down by the seashore"
			],
			"links" : 
			[
				{
				"value" : "http://example.com/entity/XXXX",
				"rel" : "self",
				"href" : "http://example.com/entity/XXXX"
				}
			],
			"registrationDate" : "1990-12-31T23:59:60Z",
			"lastChangedDate" : "1990-12-31T23:59:60Z",
			"lastChangedBy" : "joe@bob.com"
		}"""
		reslt = objects.entity(  # status
			'XXXX',
			['Joe Bob, Inc.', 'Bobby Joe Shopping'],
			None,
			'registrant',
			['123 Maple Ave', 'Suite 90001', 'Vancouver', 'BC', '12393'],
			['joe@bob.com', 'bob@joe.com'],
			{'office': ['1-958-555-4321', '1-958-555-4322'], 'fax': ['1-958-555-4323'], 'mobile': ['1-958-555-4324']},
			['she sells seas shells', 'down by the seashore'],
			{'value': 'http://example.com/entity/XXXX', 'rel': 'self', 'href': 'http://example.com/entity/XXXX'},
			registrationDate='1990-12-31T23:59:60Z',
			lastChangedDate='1990-12-31T23:59:60Z',
			lastChangedBy='joe@bob.com',
			)
		self.assertJSON(reslt, answer)


class NameserverTest(WeirdsTestCase):

	def test_exampleNameserver(self):
		answer = \
   """{
			"handle" : "XXXX",
			"name" : "ns1.example.com",
			"status" : [ "active" ],
			"ipAddresses" : [ "192.0.2.1", "192.0.2.2" ],
			"remarks" : 
			[
			"she sells seas shells",
			"down by the seashore"
			],
			"links" : 
			[
			{
				"value" : "http://example.net/nameserver/xxxx",
				"rel" : "self",
				"href" : "http://example.net/nameserver/xxxx"
			}
			],
			"port43" : "whois.example.net",
			"registrationDate" : "1990-12-31T23:59:60Z",
			"registrationBy" : "ABC123",
			"lastChangedDate" : "1990-12-31T23:59:60Z",
			"lastChangedBy" : "ABC123",
			"sponsoredBy" : "SponsorXYZ",
			"resoldBy" : "ResellerPDQ"
			}
		"""
		reslt = objects.nameserver(
			'XXXX',
			'ns1.example.com',
			'active',
			['192.0.2.1', '192.0.2.2'],
			['she sells seas shells', 'down by the seashore'],
			{'value': 'http://example.net/nameserver/xxxx', 'rel': 'self', 'href': 'http://example.net/nameserver/xxxx'},
			port43='whois.example.net',
			registrationDate='1990-12-31T23:59:60Z',
			registrationBy='ABC123',
			lastChangedDate='1990-12-31T23:59:60Z',
			lastChangedBy='ABC123',
			sponsoredBy='SponsorXYZ',
			resoldBy='ResellerPDQ',
			)
		self.assertJSON(reslt, answer)

	def test_nameonlyNameserver(self):
		self.assertJSON(objects.nameserver(None, 'ns1.example.com'), '{"name":"ns1.example.com"}')

	def test_simpleNameserver(self):
		self.assertJSON(objects.nameserver(None, 'ns1.example.com', None, ['2001:db8::123', '2001:db8::124']),
                  '{"name": "ns1.example.com", "ipAddresses":[ "2001:db8::123", "2001:db8::124" ]}')


class DomainTest(WeirdsTestCase):

	def test_rirDomain(self):
		answer = \
   """{
		"handle" : "XXXX",
		"name" : "192.in-addr.arpa",
		"nameServers" : [ 
			{ "name" : "ns1.rir.net" }, 
			{ "name" : "ns2.rir.net" }
		],
		"delegationKeys" : [ {
			"algorithm": 7,
			"digest" : "E68C017BD813B9AE2F4DD28E61AD014F859ED44C",
			"digestType" : 1,
			"keyTag" : 53814
		}],
		"remarks" : [
			"she sells seas shells",
			"down by the seashore"
		],
		"links" : [	{
			"value": "http://example.net/domain/XXXX",
			"rel" : "self",
			"href" : "http://example.net/domain/XXXX"
		} ],
		"registrationDate" : "1990-12-31T23:59:60Z",
		"lastChangedDate" : "1990-12-31T23:59:60Z",
		"lastChangedBy" : "joe@bob.com",
		"entities" : [	{
			"handle" : "XXXX",
			"entityNames": [ "Joe Bob, Inc.", "Bobby Joe Shopping" ],
			"roles" : [ "registrant" ],
			"postalAddress" :  ["123 Maple Ave", "Suite 90001", "Vancouver", "BC", "12393" ],
			"emails" : [ "joe@bob.com", "bob@joe.com" ],
			"phones" : { 
				"office" : [ "1-958-555-4321", "1-958-555-4322" ],
				"fax" :    [ "1-958-555-4323" ],
				"mobile" : [ "1-958-555-4324" ]  
			},
			"remarks" : [
				"she sells seas shells",
				"down by the seashore"
			],
			"links" : [	{
				"value": "http://example.net/entity/xxxx",
				"rel" : "self",
				"href" : "http://example.net/entity/xxxx"
			} ],
			"registrationDate" : "1990-12-31T23:59:60Z",
			"lastChangedDate" : "1990-12-31T23:59:60Z",
			"lastChangedBy" : "joe@bob.com"
		} ]
		}
		"""

		reslt = objects.domain('XXXX', '192.in-addr.arpa', None, None, [objects.nameserver(None, 'ns1.rir.net'), objects.nameserver(None, 'ns2.rir.net')], 
							objects.entity('XXXX',
                         ['Joe Bob, Inc.', 'Bobby Joe Shopping'], 
                         None,
                         'registrant', 
                         ['123 Maple Ave', 'Suite 90001', 'Vancouver', 'BC', '12393'], 
                         ['joe@bob.com', 'bob@joe.com'], 
                         {'office': ['1-958-555-4321', '1-958-555-4322'], 'fax': ['1-958-555-4323'], 'mobile': ['1-958-555-4324']},
                         ['she sells seas shells', 'down by the seashore'],
                         objects.link("http://example.net/entity/xxxx", "self"),
								registrationDate= "1990-12-31T23:59:60Z",
								lastChangedDate= "1990-12-31T23:59:60Z",
								lastChangedBy= "joe@bob.com"
                     ),
                     objects.delegationKey(7, 'E68C017BD813B9AE2F4DD28E61AD014F859ED44C', 1, 53814),
                     ['she sells seas shells', 'down by the seashore'],
                     objects.link('http://example.net/domain/XXXX', 'self'),
                     registrationDate='1990-12-31T23:59:60Z',
                     lastChangedDate='1990-12-31T23:59:60Z',
                     lastChangedBy='joe@bob.com')
		self.assertJSON(reslt, answer)


## TODO: more tests from RFC when one is published