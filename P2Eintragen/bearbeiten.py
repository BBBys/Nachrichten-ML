import logging
import mysql.connector

from dbparam import *

PART = "\t"
WEG = "'\n"
kTitel = "title"
kUpdatet = "updated_parsed"


def speichern(titel, meldung, link, cursor, quelle, zeit):
    """
    Hash berechnen,
    Titel, Meldung und Hash eintragen
    mit Hash: Zeit, Quelle, Link nachtragen

    Args:
        titel (_type_): _description_
        meldung (_type_): _description_
        link (_type_): _description_
        cursor (_type_): _description_
        quelle (_type_): _description_
        zeit (_type_): _description_

    Returns:
        _type_: False, wenn Fehler, sonst True
    """
    logging.debug("bearbeiten:speichern:Start...")
    # titel und meldung d�rfe kein >'< enthalten
    titel = titel.replace("'", "").strip()
    meldung = meldung.replace("'", "").strip()
    hwert = hash(titel + meldung)
    try:
        sql = "INSERT INTO %s (hash,titel,meldung) VALUES ('%d','%s', '%s');" % (
            DBTMELDUNGEN,
            hwert,
            titel,
            meldung,
        )
        # logging.debug(sql)
        cursor.execute(sql)
        # sql="UPDATE  {pTabelle} SET category='{pcategory}' WHERE titel='{ptitel}'"
        # datum: {dt:yyyy-M-dd HH:mm:ss}
        if len(zeit) > 5:
            sql = f"UPDATE {DBTMELDUNGEN} SET datum='{zeit}' WHERE hash='{hwert}';"
            cursor.execute(sql)
        sql = f"UPDATE {DBTMELDUNGEN} SET quelle= '{quelle}' WHERE hash={hwert};"
        cursor.execute(sql)
        if len(link) > 7:  # http:// = 7
            sql = f"UPDATE {DBTMELDUNGEN} SET link= '{link}' WHERE hash={hwert};"
            cursor.execute(sql)

        logging.debug("bearbeiten:speichern: alles fertig")

    except mysql.connector.errors.Error as e:
        logging.error(sql)
        match e.errno:
            case 1064:
                print("Syntax Error: {}".format(e))
            case 1146:
                logging.fatal("DB nicht vorhanden: {}".format(e))
            case 1292:
                logging.error(f"Zeitangabe: {zeit}")
            case _:
                logging.fatal(e)
        return False

    return True


def bearbeiten(auftrag, db):
    ID = auftrag[0]
    Datei = auftrag[1]
    AuftragQuelle = auftrag[2]
    AuftragZeit = auftrag[3]
    with db.cursor() as cursor:
        with open(Datei, "rt") as file:
            data = ""
            i = 0
            ok = hatZeit = hatMeldung = hatTitel = False
            titel = meldung = link = AuftragQuelle = AuftragZeit = ""
            for line in file:
                teile = line.partition(PART)
                logging.debug(teile)
                key = teile[0].strip(WEG)
                val = teile[2].strip(WEG)
                match key:
                    case "-----":
                        # neuer Eintrag beginnt
                        if hatTitel:
                            ok = speichern(
                                titel, meldung, link, cursor, AuftragQuelle, AuftragZeit
                            )
                            if not ok:
                                logging.warning(f"Fehler bein Speichern von {titel}")
                                return False
                            hatTitel = hatLink = hatZeit = hatMeldung = False
                            link = ""
                            titel = ""
                    case "title":
                        titel = val
                        hatTitel = True
                    case "summary":
                        meldung = val
                        hatMeldung = True
                    case "updated_parsed":
                        pass
                    case "published_parsed":
                        pass
                    case "link":
                        link = val
                        hatLink = True
                    case _:
                        logging.error(
                            "bearbeiten:bearbeiten:match unbekannt: Key >%s< in >%s<",
                            key,
                            val,
                        )
                        raise Exception(
                            f"beim Untersuchen der RSS-Einträge\nwurde der Key {key}\nam Zeilenanfang nicht erkannt\n\nDAS VERHINDERT ALLE FOLGENDEN AUSWERTUNGEN!!"
                        )
                        return False
                        # kein commit

            # for line
    # with cursor
    logging.debug("Datei fertig")
    db.commit()
    return True
