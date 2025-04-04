#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  P21Stop.py
#  
from dbparam import DBTBB,DBHOST,DBNAME, DBUSER, DBPORT, DBPWD
#from bearbeiten import bearbeiten
#from dbroutinen import dbcreate
import mysql.connector
import logging,argparse,os
from verdichten import verdichten
from kopieren   import kopieren
from dbroutinen import zurücksetzenDaten

STOPPFILE=''
TITEL='P21Stop'
ZURÜCK=False

def main():
    try:
        db =mysql.connector.connect(host=DBHOST,db=DBNAME,user = DBUSER, port = DBPORT, password = DBPWD)  #+ ";ConvertZeroDateTime=True;", 
        if ZURÜCK:
            logging.info("Zurücksetzen")
            zurücksetzenDaten(TITEL,db)
            logging.info('...Ende')
            return 11

        if not os.path.exists(STOPPFILE):raise Exception(f'Stoppfile {STOPPFILE} fehlt')
        with db.cursor() as cursor:
            SQL = f"SELECT id FROM {DBTBB} WHERE programm='{TITEL}';"
            cursor.execute(SQL) 
            Aufträge=cursor.fetchall()
            logging.debug('%d Auftrag-Records'%len(Aufträge))

            if len(Aufträge)<1:#es muss Records geben
                logging.info('für %s liegt nichts vor'%TITEL)
                return 0
           
        Auftrag=Aufträge[0]
        logging.debug(Auftrag)
        ID=Auftrag[0]
        logging.info(f"Start {TITEL} Auftrag {ID}")
        ok=verdichten(db)
        if ok:
            db.commit()
            (ok,nRest)=kopieren(db,STOPPFILE,MAXMLD)
            logging.debug(f"Ergebnis: {ok},{nRest}")
            if ok:
                with db.cursor() as cursor:
                    if nRest<1: #alles verarbeitet
                        SQL = f"delete from {DBTBB} where programm='{TITEL}';"
                        cursor.execute(SQL) 
                        SQL=f"insert into {DBTBB} (programm) values ('P31Worter');"
                    else: 
                        logging.warning(f"es verbleiben noch {nRest} Meldungen")
                        SQL=f"insert into {DBTBB} (programm) values ({TITEL});"
                    cursor.execute(SQL)                    
                db.commit()
    except mysql.connector.errors.Error as e:
            logging.error(f"MySQL Error\n{e}")
            match e.errno:
                case 1064: 
                    print("Syntax Error: {}".format(e))
                case 1146: 
                    logging.warning("DB nicht vorhanden: {}".format(e))
                    #dbcreate(mycursor,DBTSTOPP)
                    #dbcreate(mycursor,DBTDATEN)
                case _:
                    logging.fatal(e)
            return 'SQL-Fehler'
    except Exception as e:
        logging.fatal(f"P21Stop: Exception \n{e}")
        return 'Fehler'
    return 0


if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser(
                    prog=TITEL,
                    description=
                    'Meldungen aufräumen, Stoppliste anwenden, in daten übertragen')    
    parser.add_argument(dest="pStopp",help="Datei mit Stoppwörtern")
    parser.add_argument("-m","--max",required=False,dest="pMaxMld",help="maximal behandelte Meldungen",default=2000)
    parser.add_argument("-v", "--verbose", dest="pVerbose", action='store_true', 
                        help="Debug-Ausgabe")
    parser.add_argument("-z", "--zurücksetzen", dest="pZurck", action='store_true', 
                        help="Daten löschen, neues Kopieren ermöglichen")

    arguments = parser.parse_args()
    ZURÜCK=arguments.pZurck
    Dbg= arguments.pVerbose
    MAXMLD=int( arguments.pMaxMld)
    STOPPFILE=arguments.pStopp
    if Dbg:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info(f'Start {TITEL} mit Stoppfile {STOPPFILE}, max. {MAXMLD}')

    sys.exit(main())
