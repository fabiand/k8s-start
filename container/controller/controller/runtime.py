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
    VM_RC_SPEC = """
apiVersion: v1
kind: ReplicationController
metadata:
  name: compute-rc-{DOMNAME}
  labels:
    app: compute-rc
    domain: {DOMNAME}
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: compute
        domain: {DOMNAME}
    spec:
      volumes:
      - name: host
        hostPath:
          path: /
      containers:
      - name: compute
        image: docker.io/fabiand/compute:latest
        securityContext:
          privileged: true
        ports:
        - containerPort: 1923
          name: spice
        - containerPort: 5900
          name: vnc
        - containerPort: 16509
          name: libvirt
        volumeMounts:
        - name: host
          mountPath: /host
        env:
        - name: LIBVIRT_DOMAIN
          value: {DOMNAME}
        - name: DOMAIN_HTTP_URL
          value: {DOMAIN_HTTP_URL}
        resources:
          requests:
            memory: "128Mi"
            cpu: "1000m"
          limits:
            memory: "1024Mi"
            cpu: "4000m"
    """

    VM_SVC_SPEC = """
apiVersion: v1
kind: Service
metadata:
  name: libvirt-{DOMNAME}
  labels:
    app: compute-service
    domain: {DOMNAME}
spec:
  selector:
    app: compute
    domain: {DOMNAME}
  type: NodePort
  ports:
  - name: libvirt
    port: 16509
    nodePort: 30001
  - name: vnc
    port: 5900
    nodePort: 30900
    """

    def list(self):
        matches = kubectl(["-l", "app=compute-rc",
                           "get", "rc", "-ojson"],
                          "items[*].metadata.labels.domain")
        return [m.value for m in matches] if matches else []

    def create(self, domname):
        def create(spec):
            env = {
                "DOMNAME": domname,
                "DOMAIN_HTTP_URL": "http://%s:%s/v2/keys/domains/%s" %
                (os.environ["CONTROLLER_SERVICE_HOST"],
                 os.environ["CONTROLLER_SERVICE_PORT_ETCD_REST"],
                    domname)}
            spec = spec.format(**env)
            print(spec)
            kubectl(["create", "-f", "-"], input=bytes(spec, encoding="utf8"))

        create(self.VM_RC_SPEC)
        create(self.VM_SVC_SPEC)

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
        return "qemu+tcp://%s:30001/system" % (node)


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
