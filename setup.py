from setuptools import setup, find_packages
import os

os.system("pip install -r requirements.txt")


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


setup(
    name='ktrack-core',
    version=read_version_number(),
    packages=find_packages(),
    package_data={
        '': ['*.yml']
    },
    url='',
    license='',
    author='Jan Honsbrok',
    author_email='',
    description='',
    entry_points={
        'console_scripts': [
            'interactive_api = scripts.interactive_api:main',
            'ktrack = scripts.ktrack_command:main',
        ]
    }
)
