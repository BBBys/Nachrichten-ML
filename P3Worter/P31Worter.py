#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  P31Worter.py
#  
from dbparam import DBTBB,DBHOST,DBNAME, DBUSER, DBPORT, DBPWD
import mysql.connector
import logging,argparse
from dbroutinen import zurücksetzenDaten,dbcreate
from wzahlen import wzahlen

ZURÜCK=False

def main():
    try:
        db =mysql.connector.connect(host=DBHOST,db=DBNAME,user = DBUSER, port = DBPORT, password = DBPWD)  #+ ";ConvertZeroDateTime=True;", 
        if ZURÜCK:
            logging.info("Zurücksetzen")
            zurücksetzenDaten("P3Worter",db,LKETTE)
            logging.info('...zurückgesetzt, Ende')
            return 0

        TITEL=f'P3{LKETTE}Worter'
        logging.info(f'Start {TITEL} für max. {MAXZEIT} Sekunden')

        with db.cursor() as cursor:
            SQL = f"SELECT id FROM {DBTBB} WHERE programm='{TITEL}';"
            cursor.execute(SQL) 
            Aufträge=cursor.fetchall()
            if len(Aufträge)<1:#es muss Records geben
                logging.info('für %s liegt nichts vor'%TITEL)
                return 0
           
        Auftrag=Aufträge[0]
        ID=Auftrag[0]
        logging.info(f"Start {TITEL} Auftrag {ID}")
        ok=wzahlen(db,LKETTE,MAXZEIT)
        if ok:
            with db.cursor() as cursor:
                SQL = f"delete from {DBTBB} where programm='{TITEL}';"
                cursor.execute(SQL)                    
                SQL=f"insert into {DBTBB} (programm) values ('P4Statistik');"
                cursor.execute(SQL)                    
            db.commit()
            logging.info(f"Auftrag {ID} erfolgreich beendet")
        else:logging.info(f"Auftrag {ID} nicht beendet")
    except mysql.connector.errors.Error as e:
            logging.error(f"MySQL Error\n{e}")
            match e.errno:
                case 1064: 
                    print("Syntax Error: {}".format(e))
                case 1146: 
                    logging.warning("DB nicht vorhanden: {}".format(e))
                    dbcreate(db,e.msg)
                    #dbcreate(mycursor,DBTDATEN)
                case _:
                    print(e.__dict__)
                    logging.fatal(e)
            return 'SQL-Fehler'
    except Exception as e:
        print(e.__dict__)
        logging.fatal(f"{TITEL}: Exception \n{e}")
        return 'Fehler'
    return 0

if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser(
                    prog="P3Worter",
                    description=
                    'Einzelwörter aus daten')    
    parser.add_argument("-v", "--verbose", dest="pVerbose", action='store_true', 
                        help="Debug-Ausgabe")
    parser.add_argument("-z", "--zurücksetzen", dest="pZurck", action='store_true', 
                        help="Einzelwörter-Daten löschen, neues Zählen ermöglichen")
    parser.add_argument("-t","--tmax",required=False,dest="pMaxZeit",
                        help="maximale Laufzeit [300] s",default=300)
    parser.add_argument("-l","--länge",required=False,dest="pLänge",
                        help="Wörter in Wortkette [1]",default=1)
    
    arguments = parser.parse_args()
    LKETTE=int( arguments.pLänge)
    MAXZEIT=int( arguments.pMaxZeit)
    ZURÜCK=arguments.pZurck
    Dbg= arguments.pVerbose
    if Dbg:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    sys.exit(main())
