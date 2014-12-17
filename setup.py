#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='xivo_dird_plugin_google_contacts',
    version='0.1',

    description='XiVO dird plugins to search in google contacts',

    author='Sylvain Boily',
    author_email='sboily@avencall.com',

    url='https://github.com/sboily/xivo-dird-plugin-backend-google-contacts',

    packages=find_packages(),

    entry_points={
        'xivo_dird.backends': [
            'gcontacts = xivo_dird_plugin_google_contacts.gcontacts_plugin:GcontactsPlugin',
        ],
    }
)
