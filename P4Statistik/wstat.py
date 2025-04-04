from dbparam import DBTW1,DBTW2,DBTW3,DBTW4,DBTW5
import mysql.connector
import logging
#from math import sqrt,ceil

def wstat(Datenbank,MAXANA):
     """
     Wörter Statistik

     Args:
          db (_type_): geöffnete Datenbank
          MAXANA (_type_): max. Meldungen
     Returns:
         _type_: _description_
     """
     logging.debug('Start wstat...')
                    
     try:
          with Datenbank.cursor() as readCursor,\
               Datenbank.cursor() as writeCursor:
               sql = f"SELECT SUM(`anzahl`),count(`anzahl`) FROM `{DBTW1}`;"
               readCursor.execute(sql)
               erg=readCursor.fetchone()
               #print(erg)
               token=int(erg[0])
               types=int(erg[1])
               logging.info(f"\n{token:7}\tToken,\n{types:7}\tTypes")
               sql = f"SELECT SUM(`anzahl`),COUNT(`anzahl`) FROM `{DBTW1}` WHERE gesamt <> {token}; "
               readCursor.execute(sql)
               erg=readCursor.fetchone()
               #print(erg)
               ntoken=int(erg[0])
               ntypes=int(erg[1])
               logging.info(f"\ndavon unbearbeitet\n{ntoken:7}\tToken,\n{ntypes:7}\tTypes ({ntypes/types:.0%})")
               return

               sql = f"SELECT count(meldung) FROM {DBTDATEN} where w1<1;"
               readCursor.execute(sql)
               nOffeneMld=readCursor.fetchone()[0]
               logging.info(f"{nOffeneMld} neue Meldungen in {nAlleMld} ({100*nOffeneMld/nAlleMld:.1f} %)")
               
               sql = f"SELECT zeigerRoh,meldung FROM {DBTDATEN} where not w1 limit {MAXANA};"
               #sql = f"SELECT meldung FROM {DBTDATEN} where w1<1 limit {MAXANA};"
               logging.debug(sql)
               readCursor.execute(sql)
               daten=readCursor.fetchall()
               logging.debug(f"SQL liefert {readCursor.rowcount} Records")
               for dat in daten:
                    #logging.debug(dat)
                    iMld=dat[0]
                    mld=dat[1]
                    #logging.debug(f"i={iMld},Mld >{mld}<")
                    ok=True
                    if ok:ok=w1zahlen(writeCursor,DBTW1, mld)
                    #if ok:ok=w2zahlen(writeCursor,DBTW2, mld)
                    if ok:ok=w3zahlen(writeCursor,DBTW3, mld)
                    #if ok:ok=w4zahlen(writeCursor,DBTW4, mld)
                    if ok:ok=w5zahlen(writeCursor,DBTW5, mld)
                    if ok:
                         sql = f"update {DBTDATEN} set w1 = 1 where zeigerRoh={iMld};"
                         writeCursor.execute(sql)
                         Datenbank.commit()
     except mysql.connector.errors.Error as e:
          logging.error(f"w1zahlen: MySQL Error {e.errno}\n{e}")
          match e.errno:
               case 1064: 
                    print("w1zahlen: Syntax Error: {}".format(e))
               case 1146: 
                    logging.warning("wzahlen: DB nicht vorhanden: {}".format(e))
                    dbcreate(Datenbank,"{}".format(e))
                    raise "Neustart notwendig"
               case _:
                    logging.fatal(f"wzahlen: {e}")
                    print(e.__dict__)
                    raise e
          return 9999
     return (nOffeneMld-MAXANA)

def w1zahlen(c,t, mld):
     for w in mld.split():
          sql = f"SELECT anzahl FROM {t} where wort='{w}';"
          c.execute(sql)
          nw=c.fetchone()
          if nw is None:
               sql = f"insert into {t} (wort) values ('{w}');"
          else:
               sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
          c.execute(sql)
     return True

def w2zahlen(c,t, mld):
     w1=None
     for w2 in mld.split():
          if w1 is not None:
               w=w1+' '+w2
               sql = f"SELECT anzahl FROM {t} where wort='{w}';"
               c.execute(sql)
               nw=c.fetchone()
               if nw is None:
                    sql = f"insert into {t} (wort) values ('{w}');"
               else:
                    sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
               c.execute(sql)
          w1=w2
     return True
    
def w3zahlen(c,t, mld):
     w1=None
     w2=None
     for w3 in mld.split():
          if w1 is not None:
               w=w1+' '+w2+' '+w3
               sql = f"SELECT anzahl FROM {t} where wort='{w}';"
               c.execute(sql)
               nw=c.fetchone()
               if nw is None:
                    sql = f"insert into {t} (wort) values ('{w}');"
               else:
                    sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
               c.execute(sql)
          w1=w2
          w2=w3
     return True
def w4zahlen(c,t, mld):
     w1=None
     w2=None
     w3=None
     for w4 in mld.split():
          if w1 is not None:
               w=w1+' '+w2+' '+w3+' '+w4
               sql = f"SELECT anzahl FROM {t} where wort='{w}';"
               c.execute(sql)
               nw=c.fetchone()
               if nw is None:
                    sql = f"insert into {t} (wort) values ('{w}');"
               else:
                    sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
               c.execute(sql)
          w1=w2
          w2=w3
          w3=w4
     return True
def w5zahlen(c,t, mld):
     w1=None
     w2=None
     w3=None
     w4=None
     for w5 in mld.split():
          if w1 is not None:
               w=w1+' '+w2+' '+w3+' '+w4+' '+w5
               sql = f"SELECT anzahl FROM {t} where wort='{w}';"
               c.execute(sql)
               nw=c.fetchone()
               if nw is None:
                    sql = f"insert into {t} (wort) values ('{w}');"
               else:
                    sql = f"update {t} set anzahl = {nw[0]+1} where wort like '{w}';"
               c.execute(sql)
          w1=w2
          w2=w3
          w3=w4
          w4=w5
     return True
