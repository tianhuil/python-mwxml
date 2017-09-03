from __future__ import absolute_import
from nose.tools import eq_

from ...element_iterator import ElementIterator
from ..user import User


def test_user():
    XML = u"""
    <contributor>
      <username>Gen0cide</username>
      <id>92182</id>
    </contributor>
    """
    user = User.from_element(ElementIterator.from_string(XML))
    eq_(user.id, 92182)
    eq_(user.text, u"Gen0cide")

    XML = u"""
    <contributor>
      <ip>192.168.0.1</ip>
    </contributor>
    """
    user = User.from_element(ElementIterator.from_string(XML))
    eq_(user.id, None)
    eq_(user.text, u"192.168.0.1")
