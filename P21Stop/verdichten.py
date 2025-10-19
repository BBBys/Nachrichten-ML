from dbparam import DBTSTOP, DBTMELDUNGEN
import mysql.connector
import logging


def verdichten(Datenbank):
    """doppelte Meldungen löschen

    Args:
        db (_type_): _description_

    Returns:
        _type_: _description_
    """
    logging.debug("Start verdichten...")
    with Datenbank.cursor() as readCursor:
        sql = f"SELECT count(titel) FROM {DBTMELDUNGEN} where status='neu';"
        readCursor.execute(sql)
        nNeue = readCursor.fetchone()[0]
        logging.info(f"{nNeue} neue Meldungen vorher")
        sql = f"SELECT hash,titel,meldung FROM {DBTMELDUNGEN} where Status='neu' order by titel,meldung;"
        logging.debug(sql)
        readCursor.execute(sql)
        alleDatenSätze = readCursor.fetchall()
        folgenderDatensatz = ("0", "x", "y")
        folgenderText = folgendeMeldung = ""
        with Datenbank.cursor() as writeCursor:
            for einDatenSatz in alleDatenSätze:
                vorhergehenderDatensatz = folgenderDatensatz
                folgenderDatensatz = einDatenSatz
                vorhergehendrText = folgenderText
                vorhergehendeMeldung = folgendeMeldung
                folgenderText = folgenderDatensatz[1].strip().lower()
                folgendeMeldung = folgenderDatensatz[2].strip().lower()
                if (
                    vorhergehendrText == folgenderText
                    and vorhergehendeMeldung == folgendeMeldung
                ):
                    sql2 = f"delete FROM {DBTMELDUNGEN} where hash = {vorhergehenderDatensatz[0]};"
                    # logging.debug(f"***\n{t1}\n{t2}\n***\n{sql2}")
                else:
                    sql2 = f"update {DBTMELDUNGEN} set status ='vereinzelt' where hash = {vorhergehenderDatensatz[0]};"
                    # logging.debug(f"***\n{t1}\n{t2}\n***\n{sql2}")
                writeCursor.execute(sql2)
        sql = f"SELECT count(titel) FROM {DBTMELDUNGEN} ;"
        readCursor.execute(sql)
        m = readCursor.fetchone()[0]
        logging.info(f"{m} Meldungen gesamt nachher ")

    return True
