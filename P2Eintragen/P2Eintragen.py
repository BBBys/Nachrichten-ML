#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  P2Eintragen.py
#  
from dbparam import *
from bearbeiten import bearbeiten
from dbroutinen import dbcreate
import mysql.connector
import logging,argparse,os

TITEL='P2Eintragen'

def main():
    try:
        mydb =mysql.connector.connect(host=DBHOST,db=DB,user = DBUSER, port = DBPORT, password = DBPWD)  #+ ";ConvertZeroDateTime=True;", 
        with mydb.cursor() as mycursor:
            SQL = "SELECT id,parameter,parameter2,zeit FROM %s WHERE programm='%s';"%(DBTBB,TITEL)
            mycursor.execute(SQL) 
            Aufträge=mycursor.fetchall()
            logging.debug('%d Records'%len(Aufträge))

            if len(Aufträge)<1:#es muss Records geben
                logging.info('für %s liegt nichts vor'%TITEL)
                return True
        #with mycursor    
        Auftrag=Aufträge[0]
        logging.debug(Auftrag)
        ID=Auftrag[0]
        Datei=Auftrag[1]
        if  os.path.exists(Datei):
            logging.info(f"Start Bearbeitung ID {ID}")
            ok=bearbeiten(Auftrag,mydb)
            if not ok:
                logging.error(f"bearbeiten von ID {ID}\n{Auftrag}")
                return False
            logging.info(f"Ende  Bearbeitung ID {ID}")
            os.remove(Datei)
        else:
            logging.error(f"Datei fehlt für ID {ID}\n{Auftrag}")
        with mydb.cursor() as mycursor:
            SQL = f"insert into {DBTBB} (programm) values ('P21Stop');"
            mycursor.execute(SQL) 
            SQL = f"delete FROM {DBTBB} WHERE id='{ID}';"
            mycursor.execute(SQL)
        #with mycursor    
        mydb.commit()  

        #es gab Aufträge



    except mysql.connector.errors.ProgrammingError as e:
            logging.error(e,stack_info=True)
            match e.errno:
                case 1064: 
                    print("Syntax Error: {}".format(e))
                case 1146: 
                    logging.warning("DB nicht vorhanden: {}".format(e))
                    dbcreate(mycursor,DBTBB)
                case _:
                    logging.fatal(e,stack_info=True)
    except Exception as e:
        logging.fatal(e,stack_info=True)
    finally:
        mydb.close()
    return 0


if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser(
                    prog=TITEL,
                    description='Zeilen aus Datei in DB aufnehmen')    
    parser.add_argument("-v", "--verbose", dest="pVerbose", action='store_true', help="Debug-Ausgabe")

    arguments = parser.parse_args()
    Dbg= arguments.pVerbose
    if Dbg:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info('Start %s'%(TITEL))
    sys.exit(main())
