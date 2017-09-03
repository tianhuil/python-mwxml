from __future__ import absolute_import
import mwtypes

from .util import consume_tags


class User(mwtypes.User):
    u"""
    User `id` and `text`.  See :class:`mwtypes.Revision.User` for a
    description of fields.
    """
    TAG_MAP = {
        u'id': lambda e: int(e.text),
        u'username': lambda e: unicode(e.text),
        u'ip': lambda e: unicode(e.text)
    }

    @classmethod
    def from_element(cls, element):
        values = consume_tags(cls.TAG_MAP, element)

        return cls(
            values.get(u'id'),
            values.get(u'username', values.get(u'ip'))
        )
