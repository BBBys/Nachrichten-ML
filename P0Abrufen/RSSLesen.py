import feedparser
import logging


def rsslesen(feed, aus):
    """RSS lesen und Inhalt in Datei ausgeben

    Args:
        feed (string): URL
        aus (string): Dateiname mit Pfad

    Returns:
        bool: immer True, False nur für Debug
    """
    WEG = [
        "title_detail",
        "summary_detail",
        "content",
        "published",
        "guidislink",
        "links",
        "id",
        "updated",
        "dc_format",
        "rights",
        "rights_detail",
        "language",
        "publisher",
        "publisher_detail",
        "dc_identifier",
        "dc_subjects",
        "dcterms_audience",
        "dcterms_isformatof",
        "tags",
        "updated_parsed",
        "link",
    ]
    # übrige:
    logging.debug("Feed %s lesen" % feed)
    rss = feedparser.parse(feed)
    # logging.debug(rss.channel.updated)
    logging.info(rss.feed.title)
    with open(aus, "wt") as file:
        for entry in rss.entries:
            file.write("-----\n")
            # for w in WEG:
            #    del entry[w]
            ##der Key 'tags' lässt sich direkt nicht entfernen
            # entry['tags']=''
            # del entry['tags']
            # logging.debug(entry)
            for k, v in entry.items():
                if k not in WEG:
                    file.write("'%s'\t'%s'\n" % (k, v))
        # for entry
    # with open
    return True
