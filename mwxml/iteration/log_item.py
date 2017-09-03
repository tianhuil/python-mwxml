from __future__ import absolute_import
import logging

import mwtypes

from ..errors import MalformedXML
from .page import extract_namespace
from .user import User

logger = logging.getLogger(__name__)


class LogItem(mwtypes.LogItem):
    u"""
    LogItem meta data. See :class:`mwtypes.LogItem`
    for a description of fields.

    :Example:
        .. code-block:: python

            dump = mwxml.Dump( ... )

            for log_item in dump.log_items:
                print("{0} {1}".format(log_item.id, log_item.type))
    """
    @classmethod
    def from_element(cls, element, namespace_map=None):
        id = None
        timestamp = None
        comment = None
        user = None
        page = None
        type = None
        action = None
        text = None
        params = None
        comment_deleted = None
        user_deleted = None

        for sub_element in element:
            tag = sub_element.tag
            if tag == u"id":
                id = int(sub_element.text)
            elif tag == u"timestamp":
                timestamp = mwtypes.Timestamp(sub_element.text)
            elif tag == u"comment":
                comment_deleted = sub_element.attr(u'deleted') is not None
                if not comment_deleted:
                    comment = sub_element.text
            elif tag == u"contributor":
                user_deleted = sub_element.attr(u'deleted') is not None
                if not user_deleted:
                    user = User.from_element(sub_element)
            elif tag == u"logtitle":
                if sub_element.text is None:
                    namespace = None
                    title = None
                elif namespace_map is not None:
                    namespace, title = extract_namespace(
                        sub_element.text, namespace_map)
                else:
                    namespace = None
                    title = element.text
                page = cls.Page(namespace=namespace, title=title)
            elif tag == u"type":
                type = sub_element.text
            elif tag == u"action":
                action = sub_element.text
            elif tag == u"text":
                logger.warn(u"A <text> tag was seen in a log item ... ignoring")
            elif tag == u"params":
                params = sub_element.text
            else:
                raise MalformedXML(u"Unexpected tag found when processing " +
                                   u"a <logitem>: '{0}'".format(tag))

        deleted = cls.Deleted(comment=comment_deleted, user=user_deleted)

        return cls(id=id, timestamp=timestamp, comment=comment,
                   user=user, page=page, type=type, action=action, text=text,
                   params=params, deleted=deleted)
