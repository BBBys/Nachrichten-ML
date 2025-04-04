from dbparam import DBTDATEN
import mysql.connector
import logging
from math import sqrt,ceil
from sklearn.feature_extraction.text import CountVectorizer
#from cluster import cluster

MAXANA=20000
MAXFEAT=1000#ceil(sqrt(MAXANA))

def mmextr(Datenbank):
     """
     Wörter zählen
     Merkalsextraktion

     Args:
         db (_type_): _description_

     Returns:
         _type_: _description_
     """
     logging.debug('Start W1 zählen...')
     cv=CountVectorizer(max_features=MAXFEAT,ngram_range=(1,1),analyzer='word')
   
     with Datenbank.cursor() as readCursor:
          sql = f"SELECT count(meldung) FROM {DBTDATEN} ;"
          readCursor.execute(sql)
          nAlle=readCursor.fetchone()[0]
          sql = f"SELECT count(meldung) FROM {DBTDATEN} where w1<1;"
          readCursor.execute(sql)
          nNeue=readCursor.fetchone()[0]
          logging.info(f"{nNeue} neue Meldungen in {nAlle} ({100*nNeue/nAlle:.1f} %)")
          
          sql = f"SELECT zeigerRoh,meldung FROM {DBTDATEN} where w1<1 limit {MAXANA};"
          #sql = f"SELECT meldung FROM {DBTDATEN} where w1<1 limit {MAXANA};"
          readCursor.execute(sql)
          meldungen=readCursor.fetchall()
          # meldungen erscheint in fit_transform als tupel
          
          mldListe=[]          
          for i in range(0,len( meldungen)):
              mldListe.append(meldungen[i][1])
          # mldListe hat jetzt die richtige Form 'Liste mit Strings' für fit_transform
          # jedes Listenelement ist eine Meldung
     
          typesInMld = cv.fit_transform(mldListe)
          types=cv.get_feature_names_out()
          print(types)
          # typesInMld enthält die Häufigkeiten jedes Worts in jeder Meldung:
          # [Meldungsnummer, Wortnummer]
          # types sind die Wörter: [Wortnummer], alphabetisch sortiert
          wTypes=typesInMld.shape[1]
          dSätze=typesInMld.shape[0]
          logging.info(f"w1zahlen: erfasst wurden\nWorttypes\t{wTypes} in\nDatensätzen\t{dSätze}")
          #print(typesInMld.toarray())

          sum={}
          for w in types:
               sum[w]=0
          #print(typesInMld.toarray())


          for j in range(wTypes):
               n=sum[types[j]]
               for i in range(dSätze):
                    #print(f"i={i} j={j}")
                    n+=typesInMld[i,j]
               sum[types[j]]=n

          for x in sum:
               print(f"{sum[x]}\t{x}")

          g=0
          for x in sum.values():
               g+=x
          print(g)



          return False
     
          #getnnz(dc)
          
          
          
          
          return False
          
          folgenderDatensatz=('0','x','y')
          folgenderText=folgendeMeldung=''
          with Datenbank.cursor() as writeCursor:
               for einDatenSatz in meldungen:
                    vorhergehenderDatensatz=folgenderDatensatz
                    folgenderDatensatz=einDatenSatz
                    vorhergehendrText=folgenderText
                    vorhergehendeMeldung=folgendeMeldung
                    folgenderText=folgenderDatensatz[1].strip().lower()
                    folgendeMeldung=folgenderDatensatz[2].strip().lower()
                    if vorhergehendrText==folgenderText and \
                              vorhergehendeMeldung==folgendeMeldung:
                         sql2 = \
                              f"delete FROM {DBTMELDUNGEN} where hash = {vorhergehenderDatensatz[0]};"
                         #logging.debug(f"***\n{t1}\n{t2}\n***\n{sql2}")
                    else:
                         sql2 = \
                              f"update {DBTMELDUNGEN} set status ='vereinzelt' where hash = {vorhergehenderDatensatz[0]};"
                         #logging.debug(f"***\n{t1}\n{t2}\n***\n{sql2}")
                    writeCursor.execute(sql2)
          sql = f"SELECT count(titel) FROM {DBTMELDUNGEN} ;"
          readCursor.execute(sql)
          m=readCursor.fetchone()[0]
          logging.info(f"{m} Meldungen gesamt nachher ")
          
     return True
        