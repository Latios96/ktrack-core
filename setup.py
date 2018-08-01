from setuptools import setup, find_packages
import os

os.system("pip install -r requirements.txt")

setup(
    name='ktrack-core',
    version='0.0.1',
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
