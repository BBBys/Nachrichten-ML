#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @file P31Worter.py
#   @brief Wörter oder Wortfolgen (Types: n-Gramme) zählen
#   @version V2.1
#   @date 29 Okt 2026 2025
#   @author Dr. Burkhard Borys, Zeller Ring 15, 34246 Vellmar, Deutschland
#   @copyright  Nachrichten-ML © 2025-2026 by Burkhard Borys is licensed under CC BY-NC-SA 4.0
#   https://creativecommons.org/licenses/by-nc-sa/4.0/
#   

from dbparam import DBTBB, DBHOST, DBNAME, DBUSER, DBPORT, DBPWD
import mysql.connector
import logging, argparse
from dbroutinen import zurücksetzenDaten, dbcreate
from wzahlen import wzahlen

TITEL = "P3Worter"
VERSION = "V2.1"
MACHT = "Einzelwörter und Wortfolgen aus Daten"
ZURÜCK = False


def raspberry_temperatur_anzeigen():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", encoding="ascii") as temperatur_datei:
            temperatur = int(temperatur_datei.read().strip()) / 1000
        logging.info("Raspberry-Temperatur: %.1f °C", temperatur)
    except (OSError, ValueError) as e:
        logging.debug("Raspberry-Temperatur nicht verfügbar: %s", e)


def main():
    raspberry_temperatur_anzeigen()
    try:
        db = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
        )  # + ";ConvertZeroDateTime=True;",
        if ZURÜCK:
            logging.info("Zurücksetzen")
            zurücksetzenDaten("P3Worter", db, LKETTE)
            logging.info("...zurückgesetzt, Ende")
            return 0

        TITEL = f"P3{LKETTE}Worter"
        logging.info(f"Start {TITEL} für max. {MAXZEIT} Sekunden")

        with db.cursor() as cursor:
            SQL = f"SELECT id FROM {DBTBB} WHERE programm='{TITEL}';"
            cursor.execute(SQL)
            Aufträge = cursor.fetchall()
            if len(Aufträge) < 1:  # es muss Records geben
                logging.info("für %s liegt nichts vor" % TITEL)
                return 0

        Auftrag = Aufträge[0]
        ID = Auftrag[0]
        logging.info(f"Start {TITEL} Auftrag {ID}")
        ok = wzahlen(db, LKETTE, MAXZEIT)
        if ok:
            with db.cursor() as cursor:
                SQL = f"delete from {DBTBB} where programm='{TITEL}';"
                cursor.execute(SQL)
                SQL = f"insert into {DBTBB} (programm,parameter) values ('P4Statistik', '{LKETTE}');"+\
                        f"insert into {DBTBB} (programm,parameter) values  ('P6altneu', '{LKETTE}');"
                logging.debug(SQL)
                cursor.execute(SQL)
            db.commit()
            logging.info(f"Auftrag {ID} erfolgreich beendet")
        else:
            logging.info(f"Auftrag {ID} nicht beendet")
        raspberry_temperatur_anzeigen()

    except mysql.connector.errors.Error as e:
        logging.error(f"MySQL Error\n{e}")
        match e.errno:
            case 1064:
                print("Syntax Error: {}".format(e))
            case 1146:
                logging.warning("DB nicht vorhanden: {}".format(e))
                dbcreate(db, e.msg)
                # dbcreate(mycursor,DBTDATEN)
            case _:
                print(e.__dict__)
                logging.fatal(e)
        return "SQL-Fehler"
    except Exception as e:
        print(e.__dict__)
        logging.fatal(f"{TITEL}: Exception \n{e}")
        return "Fehler"
    return 0


if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser(prog=TITEL, description=MACHT,epilog=VERSION)
    parser.add_argument(
        "-v", "--verbose", dest="pVerbose", action="store_true", help="Debug-Ausgabe"
    )
    parser.add_argument(
        "-z",
        "--zurücksetzen",
        dest="pZurck",
        action="store_true",
        help="Wörter-Daten löschen, neues Zählen ermöglichen",
    )
    parser.add_argument(
        "-t",
        "--tmax",
        required=False,
        dest="pMaxZeit",
        help="maximale Laufzeit [300] s",
        default=300,
    )
    parser.add_argument(
        "-l",
        "--länge",
        required=False,
        dest="pLänge",
        help="Wörter in Wortkette [1]",
        default=1,
    )

    arguments = parser.parse_args()
    LKETTE = int(arguments.pLänge)
    MAXZEIT = int(arguments.pMaxZeit)
    ZURÜCK = arguments.pZurck
    Dbg = arguments.pVerbose

    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO

    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt=LOG_DATEFMT)

    sys.exit(main())
