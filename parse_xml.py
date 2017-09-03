from __future__ import absolute_import
import sys
from xml.etree import ElementTree

from more_itertools import peekable


def strip_tag(tag):
    return tag.split(u"}")[1]

class Dump(object):
    __slots__ = (u'siteinfo', u'pages')

    def __init__(self, siteinfo=None, pages=None):
        self.siteinfo = siteinfo

        if pages is None:
            self.pages = xrange(0)
        else:
            self.pages = pages

    def iter(self):
        return self.pages

    @classmethod
    def from_events(cls, events):
        event, elem = events.next()
        assert event == u"start" and strip_tag(elem.tag) == u"mediawiki"


        kwargs = {}
        while events:
            event, elem = events.peek()

            # Inner loop stuff
            if event == u"start" and strip_tag(elem.tag) == u"siteinfo":
                kwargs[u'siteinfo'] = SiteInfo.from_events(events)
            elif event == u"end" and strip_tag(elem.tag) == u"siteinfo":
                #kwargs['pages'] = Page.read_from(events)
                event.next()
                break
            else:
                event.next()

        return cls(**kwargs)

    @classmethod
    def from_file(cls, f):
        events = ElementTree.iterparse(f, events=(u'start', u'end'));

        return cls.from_events(peekable(events))



class SiteInfo(object):
    __slots__ = (u'sitename', u'dbname', u'base', u'generator', u'case',
                 u'namespaces')

    def __init__(self, sitename=None, dbname=None, base=None, generator=None,
                       case=None, namespaces=None):
        self.sitename = unicode(sitename) if sitename is not None else None
        self.base = unicode(base) if base is not None else None
        self.dbname = unicode(dbname) if dbname is not None else None
        self.generator = unicode(generator) if generator is not None else None
        self.case = unicode(case) if case is not None else None
        self.namespaces = namespaces

    @classmethod
    def from_events(cls, events):
        event, elem = events.next()
        assert event == u"start" and strip_tag(elem.tag) == u"siteinfo"

        kwargs = {}
        while events:
            event, elem = events.peek()

            if event == u"end":
                if strip_tag(elem.tag) == u"sitename":
                    kwargs[u'sitename'] = elem.text
                elif strip_tag(elem.tag) == u"dbname":
                    kwargs[u'dbname'] = elem.text
                elif strip_tag(elem.tag) == u"base":
                    kwargs[u'base'] = elem.text
                elif strip_tag(elem.tag) == u"generator":
                    kwargs[u'generator'] = elem.text
                elif strip_tag(elem.tag) == u"case":
                    kwargs[u'case'] = elem.text

                events.next()

            elif event == u"start" and strip_tag(elem.tag) == u"namespaces":
                kwargs[u'namespaces'] = Namespaces.from_events(events)

            elif event == u"end" and strip_tag(elem.tag) == u"siteinfo":
                events.next()
                break
            else:
                events.next()

        return cls(**kwargs)




class Namespaces(list):

    def init(self, namespaces):
        super(Namespaces, self).__init__(namespace)

    @classmethod
    def from_events(cls, events):
        event, elem = events.next()
        assert event == u"start" and strip_tag(elem.tag) == u"namespaces"

        namespaces = cls()
        while events:
            event, elem = events.peek()

            # Inner tag stuff
            if event == u"start" and strip_tag(elem.tag) == u"namespace":
                namespaces.append(Namespace.from_events(events))
            elif event == u"end" and strip_tag(elem.tag) == u"namespaces":
                events.next()
                break
            else:
                events.next()

        return namespaces


class Namespace(object):
    __slots__ = (u'key', u'case', u'text')

    def __init__(self, key=None, case=None, text=None):
        self.key = int(key) if key is not None else None
        self.case = unicode(case) if case is not None else None
        self.text = unicode(text) if text is not None else None

    @classmethod
    def from_events(cls, events):
        event, elem = events.next()
        assert event == u"start" and strip_tag(elem.tag) == u"namespace"

        event, elem = events.next()
        assert event == u"end" and strip_tag(elem.tag) == u"namespace"

        return cls(
            elem.attrib.get(u'key'),
            elem.attrib.get(u'case'),
            elem.text
        )

dump = Dump.from_file(sys.stdin)
for ns in dump.siteinfo.namespaces:
    print ns.key
