import logging


def sauber(t, stop):
    """
    beseitigt Sonderzeichen und Stoppwörter

    Args:
        t (string): roher Text
        stop (list of strings): stoppliste

    Returns:
        string: bereinigter Text
    """
    t = " " + t.lower() + " "
    t = t.replace("&amp;", " und ")
    t = t.replace("d.h.", "das heisst")
    t = t.replace("z.b.", "zum beispiel")
    t = t.replace("ß", "ss")
    t = t.replace("ver.di", "verdi")
    t = t.replace(".", " ")
    t = t.replace("\t", " ")
    t = t.replace("#", "")
    t = t.replace("&", " ")
    t = t.replace(":", " ")
    t = t.replace("/", " ")
    t = t.replace("!", " ")
    t = t.replace(",", " ")
    t = t.replace("?", " ")
    t = t.replace("+", " ")
    t = t.replace("-", " ")
    t = t.replace("-", " ")
    t = t.replace(";", " ")
    t = t.replace("(", " ")
    t = t.replace(")", " ")
    t = t.replace("–", " ")
    t = t.replace("[", " ")
    t = t.replace("]", " ")
    t = t.replace('"', " ")
    t = t.replace("»", " ")
    t = t.replace("«", " ")

    logging.debug(f"vorher\t>{t}<")
    neu = ""
    for w in t.split():
        if w in stop:
            continue
        if not w.isnumeric():
            neu += " " + w
    logging.debug(f"nachher\t>{neu}<")

    return neu.strip()
