#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='lixplore',
    version='1.0.0',
    description='Academic Literature Search & Export CLI Tool - Search PubMed, arXiv, Crossref, DOAJ, EuropePMC with Boolean operators, smart selection, and 8 export formats',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lixplore Contributors',
    author_email='lixplore@example.com',
    url='https://github.com/yourusername/lixplore',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/lixplore/issues',
        'Source': 'https://github.com/yourusername/lixplore',
        'Documentation': 'https://github.com/yourusername/lixplore#readme',
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'lixplore=lixplore.cli:main',
        ],
    },
    python_requires='>=3.8',
    keywords='literature search academic pubmed arxiv crossref research papers export bibliography',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Text Processing :: General',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Environment :: Console',
    ],
)
