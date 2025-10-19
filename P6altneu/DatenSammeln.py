from dbparam import DBTDATEN, DBTMELDUNGEN
import mysql.connector
import logging


def DatenSammeln(Datenbank, Datei):
    logging.info("Daten werden gesammelt...")
    with Datenbank.cursor(dictionary=True, buffered=True) as curMld, Datenbank.cursor(
        dictionary=True, buffered=True
    ) as curDat:
        logging.debug("Cursor geöffnet")
        sql = f"SELECT count(meldung)as c FROM {DBTDATEN} ;"
        curMld.execute(sql)
        nAlleMld = curMld.fetchone()
        logging.info(f"{nAlleMld['c']} Meldungen insgesamt")
        sql = f"SELECT zeigerRoh as iMld,meldung as Mld FROM {DBTDATEN};"
        logging.debug(sql)
        curMld.execute(sql)
        dat = curMld.fetchone()
        with open(Datei, "w", encoding="utf-8") as f:
            while dat is not None:
                iMld = dat["iMld"]
                mld = dat["Mld"]
                sql = f"SELECT datum as d FROM {DBTMELDUNGEN} where hash = '{iMld}';"
                logging.debug(sql)
                curDat.execute(sql)
                datum = curDat.fetchone()["d"]
                f.write(datum.strftime("%y%m%d") + ";" + mld + "\n")

                dat = curMld.fetchone()
        return

        daten = curMld.fetchall()
        logging.debug(f"SQL liefert {curMld.rowcount} Records")
        for dat in daten:
            logging.debug(f"i={iMld},Mld >{mld}<")
            return
