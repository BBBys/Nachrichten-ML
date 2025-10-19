#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  P6altneu.py
#
from dbparam import DBTBB, DBHOST, DBNAME, DBUSER, DBPORT, DBPWD
import mysql.connector
import logging
from DatenSammeln import DatenSammeln
from DatenSortieren import DatenSortieren
from DatenAuswerten import analyze

TITEL = "P6altneu"


def main(Datei, Sichern, Auswerten, auchOhneAuftrag=False):
    try:
        db = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
        )
        # db.dictionary=True
        with db.cursor() as cursor:
            SQL = f"SELECT id FROM {DBTBB} WHERE programm='{TITEL}' limit 1;"
            cursor.execute(SQL)
            Aufträge = cursor.fetchall()
            if len(Aufträge) > 0:  # es muss Records geben
                Auftrag = Aufträge[0]
                ID = Auftrag[0]
                logging.info(f"Start {TITEL} Auftrag {ID}")
            else:
                logging.info("für %s liegt nichts vor" % TITEL)
                if not auchOhneAuftrag:
                    return 0
                logging.info("--- aber dennoch ausführen")

        if Sichern:
            DatenSammeln(db, Datei)
        db.close()
        if Auswerten:
            # (vorDatei,nachDatei)=DatenSortieren(Datei)
            # DatenAuserten(vorDatei,nachDatei)
            trending = analyze(Datei)  # Datei mit Datum;Schlagzeile pro Zeile
            for phrase, score, count in trending[:20]:
                print(f"{phrase}\t(Score: {score:.2f}, Count: {count})")

    except mysql.connector.errors.ProgrammingError as e:
        logging.error(e)
        match e.errno:
            case 1064:
                print("Syntax Error: {}".format(e))
    except mysql.connector.errors.Error as e:
        logging.error(f"MySQL Error\n{e}")
        match e.errno:
            case 1064:
                print("Syntax Error: {}".format(e))
            case 1146:
                logging.warning("DB nicht vorhanden: {}".format(e))
                # dbcreate(mycursor,DBTSTOPP)
                # dbcreate(mycursor,DBTDATEN)
            case _:
                logging.fatal(e)
        return "SQL-Fehler"
    # except Exception as e:
    #    logging.fatal(f"{TITEL}: Exception \n{e}")
    #    return "Fehler"
    return 0


if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(
        prog=TITEL, description="Statistik über Wörter und Trends"
    )
    parser.add_argument(
        "-v", "--verbose", dest="pVerbose", action="store_true", help="Debug-Ausgabe"
    )
    parser.add_argument(
        "-f",
        "--force",
        dest="pForce",
        action="store_true",
        help="auch, wenn nicht angefordert",
    )
    parser.add_argument(
        "-s",
        "--sichern",
        dest="pSichern",
        action="store_true",
        help="Meldungen aus Datenbank sichern",
    )
    parser.add_argument(
        "-a",
        "--auswerten",
        dest="pAuswertenn",
        action="store_true",
        help="gesicherte Meldungen auswerten",
    )
    parser.add_argument(
        dest="pDatei", nargs="?", default="./meldungen.tmp", help="Zwischendatei"
    )
    arguments = parser.parse_args()
    Dbg = arguments.pVerbose
    FORCE = arguments.pForce
    DATEI = arguments.pDatei
    SICHERN = arguments.pSichern
    AUSWERTEN = arguments.pAuswertenn
    if Dbg:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info(f"Start {TITEL}")
    sys.exit(main(DATEI, SICHERN, AUSWERTEN, FORCE))
