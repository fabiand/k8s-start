import os
import subprocess
import glob


_mount_point = '/mnt'


def create_disk(name, size):
    new_disk = "{}/{}.qcow2".format(_mount_point, name)

    if os.path.exists(new_disk):
        return {"result": "fail", "message": "disk exist"}

    args = ["qemu-img", "create", "-f", "qcow2", new_disk, "{}G".format(size)]
    try:
        subprocess.check_output(args)

    except subprocess.CalledProcessError as e:
        print(e.output)
        return {"result": "failed",
                "error-code": e.returncode}

    return {"result": "success"}


def list_disk():
    result = glob.glob("{}/*.qcow2".format(_mount_point))
    filenames = [os.path.basename(file) for file in result]
    return filenames


def delete_disk(name):
    os.remove("{}/{}".format(_mount_point, name))
    return {"result": "success"}
