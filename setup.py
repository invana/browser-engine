#!/usr/bin/env python

from setuptools import setup, find_packages

flask_server_requirements = [
    'flask>=1.1.1',
    'flask-restful>=0.3.7'
]
selenium_requirements = [
    'requests>=2.23.0'
]
setup(
    name='browser-engine',
    version='0.0.1',
    description='Web Automation and User behaviour simulations made easy with YAML configurations.',
    author='Ravi Raja Merugu',
    author_email='ravi@invanalabs.ai',
    url='https://github.com/invanalabs/browser-engine',
    packages=find_packages(
        exclude=("dist", "docs", "examples", "tests", "__experiments"),
    ),
    setup_requires=['setuptools_scm'],
    package_data={
        'browser_engine.server': [
            'static/**/*.js',
            'static/**/*.css',
            'templates/*.html',
            'templates/includes/*.html'
            '*.html',
            '*.js',
            '*.css'
        ],
    },
    include_package_data=True,
    install_requires=[
        'selenium',
        'PyYAML>=5.3.1',
        'web-parsers==0.0.2'
    ],
    entry_points={
        'console_scripts': [
            'browser-engine-start = browser_engine.server.app.run',
        ]
    },
    extras_require={
        "all": flask_server_requirements,
        "server": flask_server_requirements,
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
