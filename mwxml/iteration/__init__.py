u"""
These classes form the basis of iterative processing of XML dumps.  These
datatypes are based on those found in http://pythonhosted.org/mwtypes

.. autoclass:: mwxml.Dump
    :members:

.. autoclass:: mwxml.SiteInfo

.. autoclass:: mwxml.Page
    :inherited-members:

.. autoclass:: mwxml.LogItem
    :inherited-members:

.. autoclass:: mwxml.Revision
    :inherited-members:

.. autoclass:: mwxml.Namespace
    :inherited-members:

"""
from __future__ import absolute_import
from .dump import Dump
from .page import Page
from .log_item import LogItem
from .revision import Revision
from .site_info import SiteInfo
from .namespace import Namespace

__all__ = [Dump, Page, LogItem, Revision, SiteInfo, Namespace]
