from dbparam import DBTDATEN, DBTW1
from dbroutinen import dbcreate
import mysql.connector
import logging

# from math import sqrt,ceil


def w1zahlen(Datenbank, MAXANA):
    """
    Einzel-Wörter zählen

    Args:
         db (_type_): geöffnete Datenbank
         MAXANA (_type_): max. Meldungen
    Returns:
        _type_: _description_
    """
    logging.debug("Start W1 zählen...")
    try:
        with Datenbank.cursor() as readCursor, Datenbank.cursor() as writeCursor:
            sql = f"SELECT count(meldung) FROM {DBTDATEN} ;"
            readCursor.execute(sql)
            nAlleMld = readCursor.fetchone()[0]
            sql = f"SELECT count(meldung) FROM {DBTDATEN} where w1<1;"
            readCursor.execute(sql)
            nOffeneMld = readCursor.fetchone()[0]
            logging.info(
                f"{nOffeneMld} neue Meldungen in {nAlleMld} ({100*nOffeneMld/nAlleMld:.1f} %)"
            )

            sql = (
                f"SELECT zeigerRoh,meldung FROM {DBTDATEN} where not w1 limit {MAXANA};"
            )
            # sql = f"SELECT meldung FROM {DBTDATEN} where w1<1 limit {MAXANA};"
            logging.debug(sql)
            readCursor.execute(sql)
            daten = readCursor.fetchall()
            logging.debug(f"SQL liefert {readCursor.rowcount}")
            for dat in daten:
                # logging.debug(dat)
                iMld = dat[0]
                mld = dat[1]

                # logging.debug(f"i={iMld},Mld >{mld}<")
                for w in mld.split():
                    # print(w)
                    sql = f"SELECT anzahl FROM {DBTW1} where wort='{w}';"
                    # logging.debug(sql)
                    writeCursor.execute(sql)
                    nw = writeCursor.fetchone()
                    # logging.debug(nw)
                    if nw is None:
                        sql = f"insert into {DBTW1} (wort) values ('{w}');"
                    else:
                        sql = f"update {DBTW1} set anzahl = {nw[0]+1} where wort like '{w}';"
                    # logging.debug(sql)
                    writeCursor.execute(sql)
                sql = f"update {DBTDATEN} set w1 = 1 where zeigerRoh={iMld};"
                writeCursor.execute(sql)

            Datenbank.commit()

            return 9999
    except mysql.connector.errors.Error as e:
        logging.error(f"w1zahlen: MySQL Error {e.errno}\n{e}")
        match e.errno:
            case 1064:
                print("w1zahlen: Syntax Error: {}".format(e))
            case 1146:
                logging.warning("w1zahlen: DB nicht vorhanden: {}".format(e))
                dbcreate(Datenbank, DBTW1)
                raise "Neustart notwendig"
            case _:
                logging.fatal(f"w1zahlen: {e}")
                print(e.__dict__)
                raise e

        return 9999

    return nOffeneMld - MAXANA
