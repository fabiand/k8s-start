#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: sw=4 et sts=4
#
# fuzz
#
# Copyright (C) 2016  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Fabian Deutsch <fabiand@redhat.com>
#

from bottle import Bottle, request, response, HTTPResponse
from controller.lib import Domains


doms = Domains()
app = Bottle()


@app.error(405)
def method_not_allowed(res):
    if request.method == 'OPTIONS':
        new_res = HTTPResponse()
        new_res.set_header('Access-Control-Allow-Origin', '*')
        new_res.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        return new_res
    res.headers['Allow'] += ', OPTIONS'
    return request.app.default_error_handler(res)


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.route('/v1/domains/')
def doms_list():
    return {"available": doms.list_available(),
            "running": doms.list_running()}


@app.route('/v1/domains/<name>', method='GET')
def doms_show(name):
    return doms.show(name)


@app.route('/v1/domains/<name>/connection/uri', method='GET')
def doms_status(name):
    return doms.connection_uri(name)


@app.route('/v1/domains/<name>', method='DELETE')
def doms_delete(name):
    return doms.delete(name)


@app.route('/v1/domains/<name>', method='PUT')
def doms_create(name):
    domxml = request.body.read().decode("utf8")
    return doms.create(name, domxml)


app.run(host='0.0.0.0', port=8084, debug=True, reloader=True)
