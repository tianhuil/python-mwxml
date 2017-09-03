from __future__ import absolute_import
import os
from distutils.core import setup

from setuptools import find_packages
from io import open

about_path = os.path.join(os.path.dirname(__file__), u"mwxml/about.py")
exec(compile(open(about_path).read(), about_path, u"exec"))


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

setup(
    name=__name__,  # noqa
    version=__version__,  # noqa
    author=__author__,  # noqa
    author_email=__author_email__,  # noqa
    description=__description__,  # noqa
    url=__url__,  # noqa
    license=__license__,  # noqa
    packages=find_packages(),
    entry_points={
        u'console_scripts': [
            u'mwxml=mwxml.mwxml:main'
        ],
    },
    long_description=open(u'README.md').read(),
    install_requires=requirements(u"requirements.txt"),
    test_suite=u'nose.collector',
    classifiers=[
        u"Programming Language :: Python",
        u"Programming Language :: Python :: 3",
        u"Programming Language :: Python :: 3 :: Only",
        u"Environment :: Other Environment",
        u"Intended Audience :: Developers",
        u"License :: OSI Approved :: MIT License",
        u"Operating System :: OS Independent",
        u"Topic :: Software Development :: Libraries :: Python Modules",
        u"Topic :: Text Processing :: Linguistic",
        u"Topic :: Text Processing :: General",
        u"Topic :: Utilities",
        u"Topic :: Scientific/Engineering"
    ],
)
