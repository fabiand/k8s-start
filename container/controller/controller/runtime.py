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


import subprocess
import json
import os
from .utils import jsonpath

from jinja2 import Environment
from jinja2 import FileSystemLoader

abspath = os.path.abspath(__file__)
file_dir = os.path.dirname(abspath)
print(file_dir)
jinja_env = Environment(
    loader=FileSystemLoader('{}/templates'.format(file_dir)))


def kubectl(args, expr=None, **kwargs):
    app = os.environ.get("KUBECTL", "kubectl")
    argv = [app] + args
    print(argv)
    data = subprocess.check_output(argv, **kwargs)
    data = data.decode("utf-8")
    print(data)
    if expr:
        objs = json.loads(data)
        return jsonpath(expr, objs)
    return data

# TODO: Make next functions rest apis


def get_rc_pod_names(rc):
    pods = kubectl(
        ["describe", "pods", rc])
    names = [name.split(":")[1].strip()
             for name in pods.splitlines() if name.startswith("Name:")]
    return names


def get_pod_node(pod):
    pods = kubectl(
        ["describe", "pod", pod])
    node = [name.split(":")[1].strip().split("/")[0]
            for name in pods.splitlines() if name.startswith("Node:")]
    return node[0]


class KubeDomainRuntime():

    def list(self):
        matches = kubectl(["-l", "app=compute-rc",
                           "get", "rc", "-ojson"],
                          "items[*].metadata.labels.domain")
        return [m.value for m in matches] if matches else []

    def create(self, domname, mount_volumes):
        def create(template_name):
            template = jinja_env.get_template(template_name)
            print("MountVolumes")
            print(mount_volumes)
            yaml = template.render(name=domname, mounts=mount_volumes)
            print(yaml)
            kubectl(["create", "-f", "-"], input=bytes(yaml, encoding="utf8"))

        create("compute-service.yaml.in")
        create("compute-rc.yaml.in")

    def delete(self, domname):
        kubectl(["delete", "rc",
                 "-l", "domain=%s" % domname])

        kubectl(["delete", "svc",
                 "-l", "domain=%s" % domname])

    def connection_uri(self, domname):
        pods = get_rc_pod_names("compute-rc-%s" % (domname))
        assert len(pods) > 0
        node = get_pod_node(pods[0])
        # the port is hardcoded for now
        return "vnc://%s:30900/" % (node)


class FakeRuntime():
    running = set()

    def list(self):
        return list(self.running)

    def create(self, domname):
        self.running.add(domname)

    def delete(self, domname):
        self.running.remove(domname)

    def connection_uri(self, domname):
        return "qemu+tcp://%s/system" % domname
