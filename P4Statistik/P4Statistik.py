#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  P4Statistik.py
#  
from dbparam import DBTBB,DBHOST,DBNAME, DBUSER, DBPORT, DBPWD
import mysql.connector
import logging
from wstat import wstat
TITEL='P4Statistik'
ZURÜCK=False

def main():
    try:
        db =mysql.connector.connect(host=DBHOST,db=DBNAME,user = DBUSER, port = DBPORT, password = DBPWD)  #+ ";ConvertZeroDateTime=True;", 
        #if ZURÜCK:
        #    logging.info("Zurücksetzen")
        #    zurücksetzenDaten(TITEL,db)
        #    logging.info('...zurückgesetzt, Ende')
        #    return 0

        if not FORCE:
            with db.cursor() as cursor:
                SQL = f"SELECT id FROM {DBTBB} WHERE programm='{TITEL}' limit 1;"
                cursor.execute(SQL) 
                Aufträge=cursor.fetchall()
                if len(Aufträge)<1:#es muss Records geben
                    logging.info('für %s liegt nichts vor'%TITEL)
                    return 0
           
            Auftrag=Aufträge[0]
            ID=Auftrag[0]
            logging.info(f"Start {TITEL} Auftrag {ID}")
        else:logging.info(f"Start {TITEL} erzwungen")
        restWörter=wstat(db,MAXWRT)
        if not FORCE and restWörter<1:
            with db.cursor() as cursor:
                SQL = f"delete from {DBTBB} where programm='{TITEL}';"
                cursor.execute(SQL)                    
                SQL=f"insert into {DBTBB} (programm) values ('P4Statistik');"
                cursor.execute(SQL)                    
            db.commit()
        else:logging.info(f"... es bleiben noch {restWörter} Wörter übrig")
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
                    print(e.__dict__)
                    logging.fatal(e)
            return 'SQL-Fehler'
    except Exception as e:
        print(e.__dict__)
        logging.fatal(f"{TITEL}: Exception \n{e}")
        return 'Fehler'
    return 0

if __name__ == '__main__':
    import argparse,sys
    parser = argparse.ArgumentParser(
                    prog=TITEL,
                    description=
                    'Statistik über Wörter')    
    parser.add_argument("-v", "--verbose", dest="pVerbose", action='store_true', 
                        help="Debug-Ausgabe")
    parser.add_argument("-f", "--force", dest="pForce", action='store_true', 
                        help="auch, wenn nicht angefordert")
    parser.add_argument("-m","--max",required=False,dest="MaxWörter",
                        help="maximal behandelte Wörter [8000]",default=8000)
    
    arguments = parser.parse_args()
    MAXWRT=int( arguments.MaxWörter)
    Dbg= arguments.pVerbose
    FORCE= arguments.pForce
    if Dbg:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info(f'Start {TITEL} aus max. {MAXWRT} Wörtern')
    sys.exit(main())
