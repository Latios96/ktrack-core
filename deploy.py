from __future__ import print_function
import glob
import os
import re
import subprocess
import sys


class Wheel(object):

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.version = self._parse_version(path)

    def _parse_version(self, string):
        string = os.path.basename(string)
        return re.findall(r"(\d+)\.(\d+)\.(\d+)", string)[0]

    @property
    def version_str(self):
        return ".".join(self.version)

    def __str__(self):
        return "<Wheel path={} version={}>".format(self.path, self.version)

    def __repr__(self):
        return str(self)


def build_wheel():
    cmd = "{} setup.py bdist_wheel".format(sys.executable)
    print(cmd)
    subprocess.call(cmd)

    wheels = glob.glob("dist/ktrack_core-0.*py2-none-any.whl")
    wheels = map(Wheel, wheels)
    wheels = sorted(wheels, key=lambda x: x.version, reverse=True)
    return wheels[0]


def deploy_wheel(wheel):
    target_path = os.path.join(r'M:\Projekte\z_pipeline\ktrack', wheel.version_str, 'python2')
    cmd = "C:\\Python27\\Scripts\pip.exe install {} --target {}".format(wheel.path, target_path)
    print(cmd)
    subprocess.call(cmd)


if __name__ == '__main__':
    wheel = build_wheel()
    print(wheel)
    deploy_wheel(wheel)
