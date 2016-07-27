import json
import os
import subprocess
import urllib
import httplib2

from time import sleep
from urllib import request

from jinja2 import Environment
from jinja2 import FileSystemLoader

timeout = 120

abspath = os.path.abspath(__file__)
file_dir = os.path.dirname(abspath)
print(file_dir)
jinja_env = Environment(
    loader=FileSystemLoader('{}/templates'.format(file_dir)))


def kubectl(args, **kwargs):
    app = os.environ.get("KUBECTL", "kubectl")
    argv = [app] + args
    print(argv)
    try:
        data = subprocess.check_output(argv, **kwargs)
    except subprocess.CalledProcessError:
        return None
    data = data.decode("utf-8")
    # print(data)
    return data


def get_services():
    services = kubectl(["get", "services", "-o", "json"])
    if services is not None:
        return json.loads(services)
    return None


def is_service_exist(name):
    if kubectl(["get", "services", name]) is not None:
        return True
    return False


class VolumeWorker():

    ''' VolumeWoker creates a control instance
        If the service missing it will be created
        Otherwise the connection is tested
    '''

    def _test_connection(self):
        ''' Test the connection to  the service
        '''
        try:
            url = "http://{}.default:8084/v1/status".format(self.service_name)
            response = request.urlopen(url)
            print(response.read())
            return True
        except:
            pass
        return False

    def _create_worker(self):
        ''' Render from templates the rc and service
            Using kubectl launches them
        '''
        def create_template(template):
            worker_template = jinja_env.get_template(template)
            worker_yaml = worker_template.render(volume_name=self.volume_name)
            print(worker_yaml)
            kubectl(
                ["create", "-f", "-"],
                input=bytes(worker_yaml, encoding="utf8"))

        create_template('storage-worker.yaml.in')
        create_template('storage-worker-service.yaml.in')

    def __init__(self, volume_name):
        self.volume_name = volume_name
        self.service_name = "volume-worker-{}".format(volume_name)
        if not is_service_exist(self.service_name):
            self._create_worker()

        test_timeout = timeout
        while not self._test_connection() and test_timeout > 0:
            test_timeout = test_timeout - 1
            sleep(1)

        if test_timeout is 0:
            raise RuntimeError('can create storage manager')

    def add_disk(self, disk, size):
        params = json.dumps({"size": size})
        try:
            url = "http://{}.default:8084/v1/disks/{}".format(
                self.service_name, disk)
            req = urllib.request.Request(
                url=url,
                data=params.encode('utf-8'),
                headers={'Content-Type': 'application/json'})
            response = request.urlopen(req)
            retVal = response.read()
        except urllib.error.HTTPError as err:
            retVal = {"result": "failed", "error": "{}".format(err)}
        return retVal

    def delete_disk(self, disk):
        try:
            h = httplib2.Http()
            url = "http://{}.default:8084/v1/disks/{}".format(
                self.service_name, disk)
            (resp_headers, content) = h.request(url, "DELETE")
            retVal = content
        except urllib.error.HTTPError as err:
            retVal = {"result": "failed", "error": "{}".format(err)}
        return retVal

    def list_disks(self):
        url = "http://{}.default:8084/v1/disks/".format(self.service_name)
        try:
            response = request.urlopen(url)
            retVal = response.read()
        except HTTPError as err:
            retVal = {"result": "failed", "error": "{}".format(err)}
        print(retVal)
        return retVal
