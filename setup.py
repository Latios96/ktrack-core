from setuptools import setup, find_packages

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
    install_requires=['mongoengine', 'blinker', 'pyyaml', 'Qt.py', 'fire', 'tabulate', 'PySide', 'pytest-qt'],
    test_requires = ['pytest', 'mock', 'mongoengine', 'mongomock', 'blinker', 'pyyaml', 'Qt.py', 'fire', 'tabulate'],
    entry_points={
        'console_scripts': [
            'interactive_api = scripts.interactive_api:main',
            'ktrack_command = scripts.ktrack_command:main',
        ]
    }
)
