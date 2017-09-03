from __future__ import absolute_import
import mwtypes

from ..errors import MalformedXML
from .user import User


class Revision(mwtypes.Revision):
    u"""
    Revision metadata and text.  See :class:`mwtypes.Revision` for a
    description of fields.
    """

    @classmethod
    def from_element(cls, element):

        id = None
        timestamp = None
        user = None
        user_deleted = False
        minor = False
        comment = None
        comment_deleted = False
        text = None
        text_deleted = False
        str = None
        sha1 = None
        parent_id = None
        model = None
        format = None

        for sub_element in element:
            tag = sub_element.tag
            if tag == u"id":
                id = int(sub_element.text)
            elif tag == u"timestamp":
                timestamp = mwtypes.Timestamp(sub_element.text)
            elif tag == u"contributor":
                user_deleted = sub_element.attr(u'deleted') is not None
                if not user_deleted:
                    user = User.from_element(sub_element)
            elif tag == u"minor":
                minor = True
            elif tag == u"sha1":
                sha1 = sub_element.text
            elif tag == u"parentid":
                parent_id = sub_element.text
            elif tag == u"model":
                model = sub_element.text
            elif tag == u"format":
                format = sub_element.text
            elif tag == u"comment":
                comment_deleted = sub_element.attr(u'deleted') is not None
                if not comment_deleted:
                    comment = sub_element.text
            elif tag == u"text":
                text_deleted = sub_element.attr(u'deleted') is not None
                if not text_deleted:
                    text = sub_element.text
                str = sub_element.attr(u'bytes')
            else:
                raise MalformedXML(u"Unexpected tag found when processing " +
                                   u"a <revision>: '{0}'".format(tag))

        deleted = cls.Deleted(comment=comment_deleted, text=text_deleted,
                              user=user_deleted)

        return cls(
            id, timestamp,
            user=user,
            minor=minor,
            str=str,
            sha1=sha1,
            parent_id=parent_id,
            model=model,
            format=format,
            comment=comment,
            text=text,
            deleted=deleted
        )
