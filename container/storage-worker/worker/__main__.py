from bottle import Bottle, request, response
import os
import subprocess
import glob

app = Bottle()
volume_mount = "/mnt"

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


@app.route('/v1/version')
def version():
    return {"version" : "v1.0"}


@app.route('/v1/disk/<name>', method='POST')
def create(name):
    assert name.isalpha()
    new_disk = "{}/{}.qcow2".format(volume_mount,name)

    if os.path.exists(new_disk):
        return {"result":"fail" , "message":"disk exist"}

    args = ["qemu-img","create", "-f","qcow2",new_disk,"20G"]
    try:
        subprocess.check_output(args)

    except subprocess.CalledProcessError as e:
        return {"result":"failed" , "message": e.output , "error-code": e.returncode }

    return {"result":"success"}

@app.route('/v1/disks')
def list():
    result = glob.glob("{}/*.qcow2".format(volume_mount))
    filenames = [ os.path.basename(file) for file in result ];
    return {"result": filenames }

app.run(host='0.0.0.0', port=8084, debug=True, reloader=True)
