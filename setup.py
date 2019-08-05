# -*- coding: utf8 -*-
#!/usr/bin/env python
"""
ovhctl

This tool is a for act on ovh api

Licence
```````
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__author__ = "David ALEXANDRE <david.alexandre@sysscale.com>"

from setuptools import setup, find_packages

from ovhctl.release import __version__

requirements = [
    "colorlog",
    "docopt",
    "ovh",
    "PyYaml",
    "request",
    "tabulate"
]

setup(
    name='ovhctl',
    version=__version__,
    description="Client for OVH API Rest",
    long_description=open('README.md').read(),
    author="David ALEXANDRE",
    author_email="david.alexandre@bluelabs.fr",
    license="""Licensed under the Apache License, Version 2.0 (the "License")""",
    keywords=["OVH", "API"],
    packages=find_packages(),
    package_data = { '': ['README.md']},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ovhctl=ovhctl.main:main'
        ],
    }
)