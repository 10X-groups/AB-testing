#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['pandas>=1.1.0', 'numpy>=1.19.0', ]

test_requirements = ['pytest>=3', ]

setup(
    authors=['Birtuhan Kuma', 'Fisseha Estifanos', 'Hanna Desta', 'Yohanes Gutema'],
    emails=['birtukankuma1113@gmail.com', 'fisseha.137@gmail.com', 'hnnadesta@gmail.com', 'yohgut@gmail.com'],
    githubprofiles = ['https://github.com/BirtukanK', 'https://github.com/fisseha-estifanos', '', 'https://github.com/Yohanes-GR'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A repository to collaborate, code and track the week 2 group work assignment (Ab hypothesis testing) of 10 academy batch VI intensive training.",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='scripts',
    name='scripts',
    packages=find_packages(include=['scripts', 'scripts.*']),
    #test_suite='tests',
    #tests_require=test_requirements,
    url='https://github.com/10X-groups/AB-testing',
    version='0.1.0',
    zip_safe=False,
)
