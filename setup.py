#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='browser-engine',
    version='0.0.15',
    description='Web Automation and User behaviour simulations made easy with YAML configurations.',
    author='Ravi Raja Merugu',
    author_email='ravi@invanalabs.ai',
    url='https://github.com/invanalabs/browser-engine',
    packages=find_packages(
        exclude=("dist", "docs", "examples", "tests", "__experiments"),
    ),
    setup_requires=['setuptools_scm'],

    # package_data={
    #     'browser_engine.server': [
    #         'static/**/*.js',
    #         'static/**/*.css',
    #         'templates/*.html',
    #         'templates/includes/*.html'
    #         '*.html',
    #         '*.js',
    #         '*.css'
    #     ],
    # },
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restful',
        # 'uwsgi',
        'selenium',
        'pyyaml',
        'extraction-engine'

    ],
    entry_points={
        'console_scripts': [
            # 'browser-engine = browser_engine.server.app.run',
        ]
    },
)
