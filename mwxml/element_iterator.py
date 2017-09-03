from __future__ import absolute_import
import io
from xml.etree.ElementTree import ParseError

from .errors import MalformedXML

try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree


def trim_ns(tag):
    return tag[tag.find(u"}") + 1:]


class EventPointer(object):
    def __init__(self, etree_events):
        self.tag_stack = []
        self.etree_events = etree_events

    def next(self):
        event, element = self.etree_events.next()

        tag = trim_ns(element.tag)

        if event == u"start":
            self.tag_stack.append(tag)
        else:
            if self.tag_stack[-1] == tag:
                self.tag_stack.pop()
            else:
                raise MalformedXML(u"Expected {0}, but saw {1}.".format(
                    self.tag_stack[-1],
                    tag)
                )

        return event, element

    def depth(self):
        return len(self.tag_stack)

    @classmethod
    def from_file(cls, f):
        return EventPointer(etree.iterparse(f, events=(u"start", u"end")))


class ElementIterator(object):
    def __init__(self, element, pointer):
        self.pointer = pointer
        self.element = element
        self.depth = pointer.depth() - 1

        self.done = False

    def __iter__(self):

        while not self.done and self.pointer.depth() > self.depth:
            event, element = self.pointer.next()

            if event == u"start":
                sub_iterator = ElementIterator(element, self.pointer)

                yield sub_iterator

                sub_iterator.clear()

        self.done = True

    def complete(self):

        while not self.done and self.pointer.depth() > self.depth:
            event, element = self.pointer.next()
            if self.pointer.depth() > self.depth:
                element.clear()

        self.done = True

    def clear(self):
        self.complete()
        self.element.clear()

    def attr(self, key, alt=None):
        return self.element.attrib.get(key, alt)

    def __getattr__(self, attr):
        if attr == u"tag":
            return trim_ns(self.element.tag)
        elif attr == u"text":
            self.complete()
            return self.element.text
        else:
            raise AttributeError(u"{0} has no attribute {1}"
                                 .format(self.__class__.__name__, attr))

    @classmethod
    def from_file(cls, f):

        try:
            pointer = EventPointer.from_file(f)
            event, element = pointer.next()
            return cls(element, pointer)
        except ParseError, e:
            raise ParseError(u"{0}: {1}..."
                             .format(unicode(e),
                                     f.read(500)))

    @classmethod
    def from_string(cls, string):
        f = io.StringIO(string)

        return cls.from_file(f)
