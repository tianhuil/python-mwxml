from __future__ import absolute_import
import mwcli

router = mwcli.Router(
    u"mwxml",
    u"This script provides access to a set of utilities for extracting " +
        u"content from MediaWiki XML dumps.",
    {u'dump2revdocs': u"Converts XML dumps to revision documents (XML --> JSON)",
     u'validate': u"Compares a stream of revision documents against a schema",
     u'normalize': u"Converts a stream of old revision documents to documents " +
                  u"that validate against the current schema",
     u'inflate': u"Converts a stream of flat revision documents to standard " +
                u"revision documents"}
)

main = router.main
