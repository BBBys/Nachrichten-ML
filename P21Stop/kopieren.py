from dbparam import DBTSTOP,DBTMELDUNGEN,DBTDATEN
from bereinigen import sauber
import mysql.connector
import logging

def kopieren(db,stf,MAXMLD):
    """
    Titel und Meldung zusammenfassen, Sonderzeichen und Stoppwörter endfernen,
    in Kleinschreibung umwandelt, in Tabelle daten speichern

    Args:
        db (_type_): Datenbank
        stf (_type_): Pfad zu Stoppwörtern

    Raises:
        e: fängt 'doppelter Hash' ab, alles andere nicht

    Returns:
        _type_: True, wenn erledigt
    """
    logging.debug('Start kopieren...')

    with open(stf,'rt') as file:stop=file.readlines()
    # beseitigt newline am Ende:
    for i in range(len(stop)):stop[i]=stop[i].strip()

    with db.cursor() as cursor:
        sql = f"SELECT count(titel) FROM {DBTMELDUNGEN} where status = 'vereinzelt';"
        cursor.execute(sql)
        nMeldungen=cursor.fetchone()[0]
        logging.info(f"kopieren: {nMeldungen} Meldungen zum kopieren")
        if nMeldungen<1:return (True,nMeldungen)

        sql = f"SELECT hash,titel,meldung FROM {DBTMELDUNGEN} where status = 'vereinzelt' limit {MAXMLD};"
        logging.debug(sql)
        cursor.execute(sql)
        daten=cursor.fetchall()
        logging.debug(f"kopieren: {len(daten)} Daten")
        try:
            eintrag=0
            for d in daten:
                try:
                    hashAlt=d[0]
                    t=sauber(d[1],stop)+" "+sauber(d[2],stop)
                    
                    #if t.count(' die ')>0:print(f'***\n{d[1]}\n{d[2]}\n{t}')
                    sql=\
                    f"INSERT INTO {DBTDATEN} (zeigerRoh,meldung) VALUES ({hashAlt},'{t}'); "
                    eintrag=eintrag+1
                    cursor.execute(sql)
                    sql=f"update {DBTMELDUNGEN} set status='kopiert' where hash={hashAlt}; "
                    cursor.execute(sql)
                except mysql.connector.errors.Error as e:
                    logging.warning('kopieren: SQL-Exception')
                    match e.errno:
                        case 1062: 
                            logging.warning(f"kopieren: doppelter Eintrag: {t}, übersprungen und weiter")
                        case _:
                                raise e
                #try exc
            #for
            db.commit()
        except mysql.connector.errors.Error as e:
            logging.error(f"kopieren: MySQL Error Eintrag {eintrag} SQL={sql}")
            match e.errno:
                case 1064: 
                    logging.error(f"Syntax Error:\n{e}")
                case 1146: 
                    logging.warning("DB nicht vorhanden: {}".format(e))
                    #dbcreate(mycursor,DBTSTOPP)
                    #dbcreate(mycursor,DBTDATEN)
                case _:
                    logging.fatal(e)
        except Exception as e:
            logging.fatal(f"Kopieren: Exception \n{e}")
            return (False,nMeldungen)           
    logging.info('...kopieren beendet')
    return (True,(nMeldungen-MAXMLD))