from bottle import Bottle, request, response, HTTPResponse
import qcow_manager

app = Bottle()


@app.error(405)
def method_not_allowed(res):
    if request.method == 'OPTIONS':
        new_res = HTTPResponse()
        new_res.set_header('Access-Control-Allow-Origin', '*')
        new_res.set_header(
            'Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        return new_res
    res.headers['Allow'] += ', OPTIONS'
    return request.app.default_error_handler(res)


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.route('/v1/version')
def version():
    return {"version": "v1.0", "service": "storage-worker"}


@app.route('/v1/status')
def status():
    return {"status": "ready"}


@app.route('/v1/disks/<name>', method='POST')
def create(name):
    size = request.json.get('size')
    print(size)
    if int(size) is 0:
        return {"result": "fail", "message": "size is not number"}
    return qcow_manager.create_disk(name, size)


@app.route('/v1/disks/')
def list():
    return {"result": qcow_manager.list_disk()}

app.run(host='0.0.0.0', port=8084, debug=True, reloader=True)
