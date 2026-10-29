#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   @file P2Eintragen.py
#   @brief Zeilen aus Datei in DB aufnehmen
#   @version V2.1
#   @date 29 Okt 2026 2025
#   @author Dr. Burkhard Borys, Zeller Ring 15, 34246 Vellmar, Deutschland
#   @copyright  Nachrichten-ML © 2025-2026 by Burkhard Borys is licensed under CC BY-NC-SA 4.0
#   https://creativecommons.org/licenses/by-nc-sa/4.0/
#   

from dbparam import *
from bearbeiten import bearbeiten
from dbroutinen import dbcreate
import mysql.connector
import logging, argparse, os

TITEL = "P2Eintragen"
VERSION = "V2.1"
MACHT = "Zeilen aus Datei in DB aufnehmen"

def main():
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DB, user=DBUSER, port=DBPORT, password=DBPWD
        )  # + ";ConvertZeroDateTime=True;",
        with mydb.cursor() as mycursor:
            SQL = "SELECT id,parameter,parameter2,zeit FROM %s WHERE programm='%s';" % (
                DBTBB,
                TITEL,
            )
            mycursor.execute(SQL)
            Aufträge = mycursor.fetchall()
            logging.debug("%d Records" % len(Aufträge))

            if len(Aufträge) < 1:  # es muss Records geben
                logging.info("für %s liegt nichts vor" % TITEL)
                return 0
        # with mycursor
        Auftrag = Aufträge[0]
        logging.debug(Auftrag)
        ID = Auftrag[0]
        Datei = Auftrag[1]
        if os.path.exists(Datei):
            logging.info(f"Start Bearbeitung ID {ID} von Datei {Datei}")
            ok = bearbeiten(Auftrag, mydb)
            if not ok:
                logging.error(f"bearbeiten von ID {ID}\n{Auftrag}")
                return False
            logging.info(f"Ende  Bearbeitung ID {ID}")
            os.remove(Datei)
        else:
            logging.error(f"Datei fehlt für ID {ID}\n{Auftrag}")
        with mydb.cursor() as mycursor:
            SQL = f"insert into {DBTBB} (programm) values ('P21Stopp');"
            mycursor.execute(SQL)
            SQL = f"delete FROM {DBTBB} WHERE id='{ID}';"
            mycursor.execute(SQL)
        # with mycursor
        mydb.commit()

        # es gab Aufträge

    except mysql.connector.errors.ProgrammingError as e:
        logging.error(e, stack_info=True)
        match e.errno:
            case 1064:
                print("Syntax Error: {}".format(e))
            case 1146:
                logging.warning("DB nicht vorhanden: {}".format(e))
                dbcreate(mycursor, DBTBB)
            case _:
                logging.fatal(e, stack_info=True)
    except Exception as e:
        logging.fatal(e, stack_info=True)
    finally:
        mydb.close()
    return 0


if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser(
        prog=TITEL,epilog=VERSION, description=MACHT
    )
    parser.add_argument(
        "-v", "--verbose", dest="pVerbose", action="store_true", help="Debug-Ausgabe"
    )

    arguments = parser.parse_args()
    Dbg = arguments.pVerbose
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    LOG_DATEFMT = "%m-%d %H:%M"
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO

    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt=LOG_DATEFMT)

    logging.info("%s %s" % (TITEL, VERSION))
    sys.exit(main())
