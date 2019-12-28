import datetime

from setuptools import setup, find_packages
import os


def read_version_number():
    import re

    VERSIONFILE = "kttk/__init__.py"
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
        return verstr.replace("__version__", "").strip()
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


def get_version_number():
    date_format = "%m/%d/%Y"
    now = datetime.datetime.now()
    day_of_changed_versioning = datetime.datetime.strptime("12/27/2019", date_format)
    days_since_versioning_changed = now - day_of_changed_versioning

    seconds_since_midnight = int(
        (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    )
    return "{}.{}.{}".format(
        0, days_since_versioning_changed.days, seconds_since_midnight
    )


setup(
    name="ktrack-core",
    version=get_version_number(),
    packages=find_packages(),
    package_data={"": ["*.yml", "*.txt"]},
    url="",
    license="",
    author="Jan Honsbrok",
    author_email="",
    description="",
    entry_points={
        "console_scripts": [
            "interactive_api = scripts.interactive_api:main",
            "ktrack = scripts.ktrack_command:main",
        ]
    },
    install_requires=[
        "mongoengine",
        "blinker",
        "pyyaml",
        "Qt.py",
        "fire",
        "tabulate",
        "typing",
        "frozendict",
        "valideer",
        "attrs",
        "faker",
        "six",
        "enum34;python_version <= '2.7'",
    ],
)
