from __future__ import absolute_import
import io

from nose.tools import eq_

from ..element_iterator import ElementIterator, EventPointer


TEST_XML = u"""
<foo>
    <bar>
        <herp>content</herp>
    </bar>
    <derp foo="bar"></derp>
</foo>
"""


def test_pointer():
    pointer = EventPointer.from_file(io.StringIO(TEST_XML))

    eq_(pointer.tag_stack, [])
    eq_(pointer.depth(), 0)

    event, element = pointer.next()
    eq_(pointer.tag_stack, [u"foo"])
    eq_(pointer.depth(), 1)
    eq_(element.tag, u"foo")
    eq_(event, u"start")

    event, element = pointer.next()
    eq_(pointer.tag_stack, [u"foo", u"bar"])
    eq_(pointer.depth(), 2)
    eq_(element.tag, u"bar")
    eq_(event, u"start")

    event, element = pointer.next()
    eq_(pointer.tag_stack, [u"foo", u"bar", u"herp"])
    eq_(pointer.depth(), 3)
    eq_(element.tag, u"herp")
    eq_(event, u"start")

    event, element = pointer.next()
    eq_(pointer.tag_stack, [u"foo", u"bar"])
    eq_(pointer.depth(), 2)
    eq_(element.tag, u"herp")
    eq_(event, u"end")

    event, element = pointer.next()
    eq_(pointer.tag_stack, [u"foo"])
    eq_(pointer.depth(), 1)
    eq_(element.tag, u"bar")
    eq_(event, u"end")

    event, element = pointer.next()
    eq_(pointer.tag_stack, [u"foo", u"derp"])
    eq_(pointer.depth(), 2)
    eq_(element.tag, u"derp")
    eq_(event, u"start")

    event, element = pointer.next()
    eq_(pointer.tag_stack, [u"foo"])
    eq_(pointer.depth(), 1)
    eq_(element.tag, u"derp")
    eq_(event, u"end")

    event, element = pointer.next()
    eq_(pointer.tag_stack, [])
    eq_(pointer.depth(), 0)
    eq_(element.tag, u"foo")
    eq_(event, u"end")

    try:
        event, element = pointer.next()
    except StopIteration:
        return True

    assert False, u"Iteration did not stop as expected."


def test_iterator():
    foo_element = ElementIterator.from_file(io.StringIO(TEST_XML))
    foo_iterator = iter(foo_element)

    bar_element = foo_iterator.next()
    bar_iterator = iter(bar_element)
    eq_(bar_element.tag, u"bar")

    herp_element = bar_iterator.next()
    eq_(herp_element.tag, u"herp")
    eq_(herp_element.text, u"content")

    derp_element = foo_iterator.next()
    eq_(derp_element.tag, u"derp")
    eq_(derp_element.attr(u"foo"), u"bar")


def test_skipping_iterator():
    foo_element = ElementIterator.from_file(io.StringIO(TEST_XML))
    foo_iterator = iter(foo_element)

    foo_iterator.next()

    derp_element = foo_iterator.next()
    eq_(derp_element.tag, u"derp")
    eq_(derp_element.attr(u"foo"), u"bar")
