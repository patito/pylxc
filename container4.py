#!/usr/bin/python3

import lxc
import uuid
import os
import subprocess
import sys
import time



CONTAINER_NAME = str(uuid.uuid1())
CLONE_NAME = str(uuid.uuid1())
RENAME_NAME = str(uuid.uuid1())

container = lxc.Container(CONTAINER_NAME)

# Try to get the host architecture for dpkg systems
arch = "amd64"
try:
    with open(os.path.devnull, "w") as devnull:
        dpkg = subprocess.Popen(['dpkg', '--print-architecture'],
                                stderr=devnull, stdout=subprocess.PIPE,
                                universal_newlines=True)

        if dpkg.wait() == 0:
            arch = dpkg.stdout.read().strip()
except:
    pass

## Create a rootfs
print("Creating rootfs using 'download', arch=%s" % arch)
options = {
    "dist": "ubuntu",
    "release": "trusty",
    "arch": arch
}
container.create("download", 0, options)
container.start()
container.wait("RUNNING", 3)

count = 0
ips = []
while not ips or count == 10:
    ips = container.get_ips()
    time.sleep(1)
    count += 1

if os.geteuid():
    print("print first")
    container.attach_wait(lxc.attach_run_command, ["/bin/bash"],
                          namespaces=(lxc.CLONE_NEWUSER + lxc.CLONE_NEWNET
                                      + lxc.CLONE_NEWUTS))
else:
    print("print second")
    container.attach_wait(lxc.attach_run_command, ["ls"],
                          namespaces=(lxc.CLONE_NEWNET + lxc.CLONE_NEWUTS))

if len(sys.argv) > 1 and sys.argv[1] == "--with-console":
    ## Attaching to tty1
    print("Attaching to tty1")
    container.console(ttynum=1)
