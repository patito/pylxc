import lxc
import os
import sys

if not os.geteuid() == 0:
    print("The use of overlayfs requires privileged containers.")
    sys.exit(1)

# Create a base container (if missing) using an Ubuntu 14.04 image
base = lxc.Container("base")
if not base.defined:
    base.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                   "release": "precise",
                                                   "arch": "i386"})

    # Customize it a bit
    base.start()
    base.get_ips(timeout=30)
    base.attach_wait(lxc.attach_run_command, ["apt-get", "update"])
    base.attach_wait(lxc.attach_run_command, ["apt-get", "dist-upgrade", "-y"])

    if not base.shutdown(30):
        base.stop()

# Clone it as web (if not already existing)
web = lxc.Container("web")
if not web.defined:
    # Clone base using an overlayfs overlay
    web = base.clone("web", bdevtype="overlayfs",
                     flags=lxc.LXC_CLONE_SNAPSHOT)

    # Install apache
    web.start()
    web.get_ips(timeout=30)
    web.attach_wait(lxc.attach_run_command, ["apt-get", "update"])
    web.attach_wait(lxc.attach_run_command, ["apt-get", "install",
                                             "apache2", "-y"])

    if not web.shutdown(30):
        web.stop()

# Create a website container based on the web container
mysite = web.clone("mysite", bdevtype="overlayfs",
                   flags=lxc.LXC_CLONE_SNAPSHOT)
mysite.start()
ips = mysite.get_ips(family="inet", timeout=30)
if ips:
    print("Website running at: http://%s" % ips[0])
else:
    if not mysite.shutdown(30):
        mysite.stop()
