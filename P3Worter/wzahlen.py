from dbparam import DBTDATEN, DBTW1, DBTW2, DBTW3, DBTW4, DBTW5
from dbroutinen import dbcreate
import mysql.connector
import logging, time


def wzahlen(Datenbank, lkette, maxzeit):
    """
    Einzel-Wörter zählen

    Args:
         db (_type_): geöffnete Datenbank
         MAXANA (_type_): max. Meldungen
    Returns:
        _type_: _description_
    """
    logging.debug("Start W zählen...")

    try:
        with Datenbank.cursor() as readCursor, Datenbank.cursor() as writeCursor:
            worttyp = f"w{lkette}"
            sql = f"SELECT count(meldung) FROM {DBTDATEN} ;"
            readCursor.execute(sql)
            nAlleMld = readCursor.fetchone()[0]
            sql = f"SELECT count(meldung) FROM {DBTDATEN} where {worttyp}<1;"
            readCursor.execute(sql)
            nOffeneMld = readCursor.fetchone()[0]
            logging.info(
                f"Typ {worttyp}: {nOffeneMld} neue Meldungen in {nAlleMld} ({100*nOffeneMld/nAlleMld:.1f} %)"
            )

            sql = f"SELECT zeigerRoh,meldung FROM {DBTDATEN} where not {worttyp};"
            # sql = f"SELECT meldung FROM {DBTDATEN} where w1<1 limit {MAXANA};"
            logging.debug(sql)
            readCursor.execute(sql)
            daten = readCursor.fetchall()
            logging.debug(f"SQL liefert {readCursor.rowcount} Records")
            startzeit = time.time()
            for dat in daten:
                # logging.debug(dat)
                iMld = dat[0]
                mld = dat[1]
                # logging.debug(f"i={iMld},Mld >{mld}<")
                match lkette:
                    case 1:
                        ok = w1zahlen(writeCursor, DBTW1, mld)
                    # if ok:ok=w2zahlen(writeCursor,DBTW2, mld)
                    case 3:
                        ok = w3zahlen(writeCursor, DBTW3, mld)
                    # if ok:ok=w4zahlen(writeCursor,DBTW4, mld)
                    case 5:
                        ok = w5zahlen(writeCursor, DBTW5, mld)
                if ok:
                    sql = f"update {DBTDATEN} set {worttyp} = 1 where zeigerRoh={iMld};"
                    writeCursor.execute(sql)
                    Datenbank.commit()
                stoppzeit = time.time()
                if (stoppzeit - startzeit) > maxzeit:
                    logging.info(f"Maximale Zeit {maxzeit} s erreicht")
                    return False
    except mysql.connector.errors.Error as e:
        logging.error(f"w*zahlen: MySQL Error {e.errno}\n{e}")
        match e.errno:
            case 1062:
                logging.warning(
                    f"w*zahlen: doppelter Key - Race Condition?\n{e.msg}\nwird beendet"
                )
            case 1064:
                print("w*zahlen: Syntax Error: {}".format(e))
            case 1146:
                logging.warning("wzahlen: DB nicht vorhanden: {}".format(e))
                dbcreate(Datenbank, "{}".format(e))
                raise "Neustart notwendig"
            case _:
                logging.fatal(f"wzahlen: {e}")
                print(e.__dict__)
                raise e
        return False
    return ok


def w1zahlen(writec, tabelle, mld):
    for wort in mld.split():
        sql = f"SELECT anzahl FROM {tabelle} where wort='{wort}';"
        writec.execute(sql)
        nw = writec.fetchone()
        if nw is None:
            sql = f"insert into {tabelle} (wort) values ('{wort}');"
        else:
            sql = f"update {tabelle} set anzahl = {nw[0]+1} where wort like '{wort}';"
        writec.execute(sql)
    return True


def w2zahlen(writec, t, mld):
    w1 = None
    for w2 in mld.split():
        if w1 is not None:
            w = w1 + " " + w2
            sql = f"SELECT anzahl FROM {t} where wort='{w}';"
            writec.execute(sql)
            nw = writec.fetchone()
            if nw is None:
                sql = f"insert into {t} (wort) values ('{w}');"
            else:
                sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
            writec.execute(sql)
        w1 = w2
    return True


def w3zahlen(writec, t, mld):
    w1 = None
    w2 = None
    for w3 in mld.split():
        if w1 is not None:
            w = w1 + " " + w2 + " " + w3
            sql = f"SELECT anzahl FROM {t} where wort='{w}';"
            writec.execute(sql)
            nw = writec.fetchone()
            if nw is None:
                sql = f"insert into {t} (wort) values ('{w}');"
            else:
                sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
            writec.execute(sql)
        w1 = w2
        w2 = w3
    return True


def w4zahlen(c, t, mld):
    w1 = None
    w2 = None
    w3 = None
    for w4 in mld.split():
        if w1 is not None:
            w = w1 + " " + w2 + " " + w3 + " " + w4
            sql = f"SELECT anzahl FROM {t} where wort='{w}';"
            c.execute(sql)
            nw = c.fetchone()
            if nw is None:
                sql = f"insert into {t} (wort) values ('{w}');"
            else:
                sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
            c.execute(sql)
        w1 = w2
        w2 = w3
        w3 = w4
    return True


def w5zahlen(c, t, mld):
    w1 = None
    w2 = None
    w3 = None
    w4 = None
    for w5 in mld.split():
        if w1 is not None:
            w = w1 + " " + w2 + " " + w3 + " " + w4 + " " + w5
            sql = f"SELECT anzahl FROM {t} where wort='{w}';"
            c.execute(sql)
            nw = c.fetchone()
            if nw is None:
                sql = f"insert into {t} (wort) values ('{w}');"
            else:
                sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
            c.execute(sql)
        w1 = w2
        w2 = w3
        w3 = w4
        w4 = w5
    return True
