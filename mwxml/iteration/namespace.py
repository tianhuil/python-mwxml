from __future__ import absolute_import
import mwtypes


class Namespace(mwtypes.Namespace):
    u"""
    See :class:`mwtypes.Namespace` for a description of fields
    """
    @classmethod
    def from_element(cls, element):
        return cls(
            element.attr(u'key'),
            element.text or u"",
            case=element.attr(u'case')
        )
