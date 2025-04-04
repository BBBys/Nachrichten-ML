#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mytest.py
#    Nachrichten-ML © 2025 by Burkhard Borys is licensed under CC BY-NC-SA 4.0 
#    https://creativecommons.org/licenses/by-nc-sa/4.0/
#    This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
import mysql.connector
import logging,argparse
from DBCreate import dbcreate
from pprint import pprint
from datetime import date,datetime,timedelta
from RSSLesen import rsslesen
Dbg=True
DBHOST='localhost'
DB='news'
DBPORT = 3306
DBUSER = 'news'
DBPWD = 'WImGfKxkx2CQ0B9'
TITEL='P0Abrufen'
VERSION='V2'
DBTBB = 'blackboard';
DSTUNDEN = 12
UrlSPIEGEL='https://www.spiegel.de/schlagzeilen/index.rss'
UrlTAGESSCHAU='https://www.tagesschau.de/newsticker.rdf'
FILENAMEMUSTER = "{pfad}{date}{quelle}.rss"
            
def EinträgeWiederherstellen(db):
    """stellt fehlende Aufträge wieder her

    Raises:
        Exception: endet immer mit Exception
    """
    logging.debug('keine 2 Records')
    with db.cursor() as cursor:
        SQL = "insert into %s (programm,parameter) values ('%s','%s')"%(DBTBB,TITEL,'Spiegel')
        cursor.execute(SQL)
        SQL = "insert into %s (programm,parameter) values ('%s','%s')"%(DBTBB,TITEL,'Tagesschau')
        cursor.execute(SQL)
    db.commit()
    raise Exception('Tabelle %s Einträge %s erzeugt - Neustart notwendig'%(DBTBB,TITEL));
    #endet hier

def dbupdate(quelle,datei,db):
    """
    wenn RSS erfolgreich in Datei übertragen, dann Datenbank:
    - alle alten Aufträge entfernen
    - Auftrag P2Eintragen erstellen, mit
        Datei, wo Feed abgelegt wurde
        Quelle
        Zeit, wann dieser Auftrag geendet ist (automatisch)
    - neuen Auftrag für dieses Programm erstellen, mit
        Quelle
        Zeit, wann dieser Auftrag geendet ist (automatisch)


    Args:
        quelle (string): RSS
        datei (string): wo abgelegt
        db (MySQL Datenbank): Datenbank
    """
    with db.cursor() as cursor:
        SQL = "delete from %s where programm='%s' and parameter='%s';"%(DBTBB,TITEL,quelle)
        logging.debug(SQL) 
        cursor.execute(SQL)
        SQL = "insert into %s (programm,parameter) values ('%s','%s')"%(DBTBB,TITEL,quelle)
        cursor.execute(SQL)
        SQL ="insert into %s (programm,parameter,parameter2) values ('P2Eintragen','%s','%s')"%(DBTBB,datei,VERSION)
        logging.debug(SQL) 
        cursor.execute(SQL)
    db.commit()
   
def Bearbeite(Auftrag,Pfad):
    """bearbeitet einen Auftrag

    Args:
        Auftrag ([]): [1] gibt die RSS-Quelle an
        Pfad (string): Pfad

    Raises:
        Exception: wenn es die gewünschte RSS nicht gibt

    Returns:
        (bool, string, string): geklappt?, RSS, Dateiname mit Pfad
    """
    quelle=Auftrag[1]
    filename = \
        FILENAMEMUSTER.format(
            pfad=Pfad,
            date=datetime.now().strftime('%Y-%m-%d-%H-%M'),
            quelle=quelle)
    ok=False
    
    match quelle:
        case 'Spiegel': ok=rsslesen(UrlSPIEGEL,filename)
        case 'Tagesschau': ok=rsslesen(UrlTAGESSCHAU,filename)
        case _: raise Exception('RSS-Quelle %s unkekannt'%(quelle))
    return (ok,quelle,filename)

def main(abstand,ausgabe ):
    """Hauptprogramm

    Args:
        ausgabe (string): Pfad mit letztem /

    Returns:
        string: Meldungen, nicht notwendig
    """
    try:
        mydb =mysql.connector.connect(host=DBHOST,db=DB,user = DBUSER, port = DBPORT, password = DBPWD)  #+ ";ConvertZeroDateTime=True;", 
        mycursor=mydb.cursor()
        SQL = "SELECT id,parameter,zeit FROM %s WHERE programm='%s';"%(DBTBB,TITEL)
        mycursor.execute(SQL) 
        Aufträge=mycursor.fetchall()
        logging.debug('%d Records'%len(Aufträge))

        if len(Aufträge)<2:#es muss 2 Records geben
            EinträgeWiederherstellen(mydb)
            return 'Datenbankfehler'
        #es gibt indestens 2 Aufträge
        maxdate=datetime.now()-timedelta(hours=abstand)
            
        Auftrag=Aufträge[0]:    # nur den ersten
        logging.debug(Auftrag)
        zeit=Auftrag[2]
        logging.info(f"{TITEL}: Start Auftrag {Auftrag[0]}")
        if(zeit<maxdate):
            (ok,ziel,datei)=Bearbeite(Auftrag,ausgabe)
            if (ok):
                dbupdate(ziel,datei,mydb)
                return  ' einen bearbeitet'
        else:
            logging.info('noch zu früh für %s'%Auftrag[1])

    except mysql.connector.errors.ProgrammingError as e:
        logging.error(e)
        match e.errno:
            case 1064: 
                print("Syntax Error: {}".format(e))
            case 1146: 
                logging.warning("DB nicht vorhanden: {}".format(e))
                dbcreate(mycursor,DBTBB)
            case _:
                logging.fatal(e)
    except Exception as e:
        logging.fatal(e)
    finally:
        mydb.close()
    return 0

if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser(
                    prog=TITEL,
                    description='RSS abrufen und in Datei schreiben')    
    #parser.add_argument("Feed",help="Feed: S[piegel] | T[agesschau]")
    parser.add_argument("Ausgabe",default='/var/news/',help="Ausgabedatei mit Pfad [/var/news/]")
    parser.add_argument("-v", "--verbose", dest="pVerbose", action='store_true', help="Debug-Ausgabe")
    parser.add_argument("-a", "--abstand", dest="hh",
                        help="min. Abstand in Stunden [12]",type=float,default=12.0)
    arguments = parser.parse_args()
    pfad=arguments.Ausgabe
    Dbg= arguments.pVerbose
    Abstand=arguments.hh
    if Dbg:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info('Start %s: RSS --> %s'%(TITEL,pfad))
    sys.exit(main(Abstand,pfad))
