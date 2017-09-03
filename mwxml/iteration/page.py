from __future__ import absolute_import
import logging

import mwtypes

from ..errors import MalformedXML
from .revision import Revision

logger = logging.getLogger(__name__)


class Page(mwtypes.Page):
    u"""
    Page meta data and a :class:`~mwxml.Revision` iterator.  Instances of
    this class can be called as iterators directly. See :class:`mwtypes.Page`
    for a description of fields.

    :Example:
        .. code-block:: python

            page = mwxml.Page( ... )

            for revision in page:
                print("{0} {1}".format(revision.id, page.id))
    """
    def initialize(self, *args, **kwargs):
        if 'revisions' in kwargs: revisions = kwargs['revisions']; del kwargs['revisions']
        else: revisions = None
        super(Page, self).initialize(*args, **kwargs)

        # Should be a lazy generator
        self.__revisions = revisions

    def __iter__(self):
        for revision in self.__revisions:
            revision.page = self
            yield revision

    def next(self):
        revision = self.__revisions.next()
        revision.page = self
        return revision

    @classmethod
    def load_revisions(cls, first_revision, element):
        if first_revision is not None:
            yield Revision.from_element(first_revision)

        for sub_element in element:
            tag = sub_element.tag

            if tag == u"revision":
                yield Revision.from_element(sub_element)
            else:
                raise MalformedXML(u"Expected to see <revision>.  " +
                                   u"Instead saw <{0}>".format(tag))

    @classmethod
    def from_element(cls, element, namespace_map=None):
        title = None
        namespace = None
        id = None
        redirect = None
        restrictions = []

        first_revision = None

        # Consume each of the elements until we see <revision> which should
        # signal the start of revision data
        for sub_element in element:
            tag = sub_element.tag
            if tag == u"title":
                page_name = sub_element.text
            elif tag == u"ns":
                namespace = int(sub_element.text)
            elif tag == u"id":
                id = int(sub_element.text)
            elif tag == u"redirect":
                redirect = sub_element.attr(u'title')
            elif tag == u"restrictions":
                restrictions.append(sub_element.text)
            elif tag == u"revision":
                first_revision = sub_element
                break
            # Assuming that the first revision seen marks the end of page
            # metadata.  I'm not too keen on this assumption, so I'm leaving
            # this long comment to warn whoever ends up maintaining this.
            elif tag == u"DiscussionThreading":
                logger.warning(
                    u"Encountered <DiscussionThreading> and skipping it ...")
            else:
                raise MalformedXML(u"Unexpected tag found when processing " +
                                   u"a <page>: '{0}'".format(tag))

        # Assuming that I got here by seeing a <revision> tag.  See verbose
        # comment above.
        revisions = cls.load_revisions(first_revision, element)

        # Normalize title and extract namespace
        mapped_namespace, title = extract_namespace(page_name, namespace_map)
        if namespace is not None and mapped_namespace != namespace:
            logger.warn(u"Namespace id conflict detected.  " +
                        u"<title>={0}, ".format(page_name) +
                        u"<namespace>={0}, ".format(namespace) +
                        u"mapped_namespace={0}".format(mapped_namespace))

        namespace = namespace or mapped_namespace

        # Construct class
        return cls(id, title, namespace, redirect=redirect,
                   restrictions=restrictions, revisions=revisions)


def normalize_title(title):
    return title.replace(u"_", u" ")


def extract_namespace(page_name, namespace_map):
    title_parts = page_name.split(u":", 1)
    if len(title_parts) == 1:
        return 0, normalize_title(page_name)
    else:
        ns_name, split_title = title_parts
        if ns_name in namespace_map:
            return namespace_map[ns_name].id, normalize_title(split_title)
        else:
            return 0, normalize_title(page_name)
