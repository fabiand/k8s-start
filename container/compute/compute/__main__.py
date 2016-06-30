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

import json
import os
import requests
import vm

from bottle import Bottle
from bottle import HTTPResponse
from bottle import request
from bottle import response


def download_vm_defenition():
    url = os.getenv("DOMAIN_HTTP_URL")
    print("Fetching URL %s" % url)
    value = requests.get(url).text

    try:
        print("Assuming etcd source, trying to parse ...")
        value = json.loads(requests.get(url).text)["node"]["value"]
        print("node value looks okay")
    except:
        print("Failed to parse json, returning raw data")

    print(value)
    return value

#TODO find how to make it thread safe
desc = download_vm_defenition()
xml = vm.render_dom(json.loads(desc))
machine = vm.LibvirtVm(xml)

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


@app.route('/v1/status')
def status():
    return {"status": "ready"}


@app.route('/v1/vm/status')
def doms_list():
    if machine is not None:
        return {"status": machine.state()}
    return {"status": "missing"}


@app.route('/v1/vm/stop', method='DELETE')
def doms_show():
    return {"status": machine.stop()}


#TODO : return some URI for console
@app.route('/v1/vm/uri', method='GET')
def doms_status(name):
    return {"status": "todo"}

app.run(host='0.0.0.0', port=8084, debug=True)
