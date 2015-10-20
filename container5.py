#!/usr/bin/python3

import lxc
import uuid
import os
import sys
import time


class Pocker(object):
    """Pocker...

    Args:
        arch (str): Image architeture.
        dist (str): Linux distribution.
        release (str): Distribution release.

    """

    CONTAINER_NAME = str(uuid.uuid1())
    CLONE_NAME = str(uuid.uuid1())
    RENAME_NAME = str(uuid.uuid1())

    def __init__(self, arch, dist, release):
        self.container = lxc.Container(self.CONTAINER_NAME)
        self.arch = arch
        self.dist = dist
        self.release = release

    def create(self):
        options = {
            "dist": self.dist,
            "release": self.release,
            "arch": self.arch
        }
        self.container.create("download", 0, options)

    def start(self):
        """Container Start. x) """
        self.container.start()
        #self.container.wait("RUNNING", 3)

    def get_ip(self):
        """Getting IP address. """
        count = 0
        ips = []
        while not ips or count == 10:
            ips = self.container.get_ips()
            time.sleep(1)
            count += 1

    def console(self):
        self.container.console(ttynum=1)

if __name__ == '__main__':
    pocker = Pocker("amd64", "ubuntu", "trusty")
    pocker.create()
    pocker.start()
    pocker.get_ip()
    pocker.console()
