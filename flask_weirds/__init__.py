#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    flask.ext.weirds
    ============================

    Flask extension to implement weirds services.

    Please follow along with documentation in weirdsapp and weirdsmodel modules to find
    detailed info about this extension.

    You can find more info about weirds on the ietf.org working group pages at
    http://datatracker.ietf.org/wg/weirds/

    Copyright (c) 2012, Dynamic Network Services, Inc. All rights reserved.
    See the included LICENSE file for licensing information.

"""

from flask.ext.weirds.objects import *
from flask.ext.weirds.weirdsapp import *
from flask.ext.weirds.weirdsmodel import *

__all__ = [
	'WeirdsResponse',
	'WeirdsApp',
	'WeirdsDataModel',
	'WeirdsError',
	'rdapConformance',
	'notice',
	'link',
	'entity',
	'nameserver',
	'delegationKey',
	'domain',
	'ip',
	'autnum',
	'errorResponse',
	]
