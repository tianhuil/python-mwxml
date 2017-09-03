from __future__ import absolute_import
from nose.tools import eq_

from ...element_iterator import ElementIterator
from ..namespace import Namespace


def test_namespace():
    XML = u'<namespace key="0" case="first-letter" />'
    namespace = Namespace.from_element(ElementIterator.from_string(XML))
    eq_(namespace.id, 0)
    eq_(namespace.name, u"")
    eq_(namespace.aliases, None)
    eq_(namespace.case, u"first-letter")
    eq_(namespace.canonical, None)

    XML = u'<namespace key="711" case="first-letter">TimedText talk</namespace>'
    namespace = Namespace.from_element(ElementIterator.from_string(XML))
    eq_(namespace.id, 711)
    eq_(namespace.name, u"TimedText talk")
    eq_(namespace.aliases, None)
    eq_(namespace.case, u"first-letter")
    eq_(namespace.canonical, None)
