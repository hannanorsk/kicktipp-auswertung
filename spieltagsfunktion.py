from typing import List, Tuple
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.indexes.datetimes import DatetimeIndex
import hilfsfunktionen
import os
import constants
import glob


def begegnungen_aktueller_spieltag(spieltag, jahr) -> List[Tuple[str, str]]:
    import urllib.request 
    begegnungen = urllib.request.urlopen('https://api.openligadb.de/getmatchdata/bl1/'+str(jahr)+'/' + str(spieltag)).read().decode()
    import json
    Spielplan_formatiert = json.loads(begegnungen)
    liste = []
    for paarungen in Spielplan_formatiert:
        eine_paarung = (paarungen['team1']['teamName'], paarungen['team2']['teamName'])
        liste.append(eine_paarung)
        
    return liste   


def path_kürzel_mannschaft_datei(kicktipp_pfad, jahr):
    dateiname_pfad = 'Kürzel_Mannschaft.xlsx'
    xlsx_path = os.path.join(kicktipp_pfad, constants.eingabe_pfad, str(jahr), dateiname_pfad)
    return xlsx_path

def path_kürzel_kicktippunkte_datei(spieltag, kicktipp_pfad, jahr):
    input_ordner_pfad = os.path.join(kicktipp_pfad, constants.eingabe_pfad, str(jahr))
    
    liste=[]
    suchmuster_dateiname = "kicktipp-*-Rangliste-Einzelwertung_"+str(spieltag)+". Spieltag*.csv"
    suchmuster_dateipfad = os.path.join(input_ordner_pfad, suchmuster_dateiname)
    for dateipfad in glob.glob(suchmuster_dateipfad):
        liste.append(dateipfad)
    if len(liste)>1:
        liste_als_string = ', '.join(liste)
        raise FileExistsError("Die Dateinamen "+liste_als_string+" sind nicht eindeutig. Der Dateipfad darf nur einmal nach dem Muster "+suchmuster_dateipfad+" vorkommen.")        
    elif len(liste)==0:
        raise FileNotFoundError("Die Datei mit dem Dateipfad nach dem Muster "+suchmuster_dateipfad+" existiert in dem Ordner "+input_ordner_pfad+ " nicht.")
    
    return liste[0]

def suche_mannschaft_fuer_kürzel(kürzel, kicktipp_pfad, jahr):
    '''
    Liest aus der Excel Datei die Kürzel aus und gibt den Mannschaftsnamen zurück
    '''
    xlsx_path = path_kürzel_mannschaft_datei(kicktipp_pfad, jahr)
    kürzel_und_mannschaft = pd.read_excel(xlsx_path)
    mannschaft = kürzel_und_mannschaft.loc[kürzel_und_mannschaft['Kürzel']==kürzel, 'Mannschaft API'].iloc[0]

    return mannschaft


def suche_kürzel_fuer_mannschaft(mannschaft, kicktipp_pfad, jahr):
    xlsx_path = path_kürzel_mannschaft_datei(kicktipp_pfad, jahr)
    kürzel_und_mannschaft = pd.read_excel(xlsx_path)
    kürzel = kürzel_und_mannschaft.loc[kürzel_und_mannschaft['Mannschaft API']==mannschaft, 'Kürzel'].iloc[0]
   
    return kürzel


def alle_kürzel(kicktipp_pfad, jahr):
    xlsx_path = path_kürzel_mannschaft_datei(kicktipp_pfad, jahr)
    kürzel_und_mannschaft = pd.read_excel(xlsx_path)
    alle_kürzel = kürzel_und_mannschaft['Kürzel'].tolist()
    return alle_kürzel


def kürzel_kicktipppunkte(spieltag, kicktipp_pfad, jahr) -> DataFrame:
    csv_path= path_kürzel_kicktippunkte_datei(spieltag, kicktipp_pfad, jahr)
    df = pd.read_csv(csv_path, usecols=['Name','Punkte'], sep=";")
    
    return df


def mannschaft_kicktipppunkte(kürzel, spieltag, kicktipp_pfad, jahr) -> Tuple[str, int]:
    '''
    Funktion soll je Kürzel die Mannschaft und ihre entsprechenden Punkte zurückgeben in einem Tuple
    '''
    mannschaftsname = suche_mannschaft_fuer_kürzel(kürzel, kicktipp_pfad, jahr)
    tipper_kicktipppunkte_tabelle = kürzel_kicktipppunkte(spieltag, kicktipp_pfad, jahr)
    kicktipppunkte_fuer_kürzel = tipper_kicktipppunkte_tabelle.loc[tipper_kicktipppunkte_tabelle['Name'] == kürzel]['Punkte'].values[0]
    kicktipppunkte = (mannschaftsname, kicktipppunkte_fuer_kürzel)
    
    return kicktipppunkte


class Vereinsinfo:
    def __init__(self, kürzel, mannschaft: str, kicktipppunkte) -> None:
        self.kürzel = kürzel
        self.mannschaft = mannschaft
        self.kicktipppunkte = kicktipppunkte

def vereinsinformationen(spieltag, kicktipp_pfad, jahr) -> List[Vereinsinfo]:
    liste=[]
    for kürzel in alle_kürzel(kicktipp_pfad, jahr):
        mannpunkt = mannschaft_kicktipppunkte(kürzel, spieltag, kicktipp_pfad, jahr)
        verein = Vereinsinfo(kürzel, mannpunkt[0], mannpunkt[1])
        liste.append(verein)

    return liste


def punktberechnung_aktueller_spieltag(team1_kicktipppunkte, team2_kicktipppunkte):
    '''
    punktberechnung berechnet die Punkte für den aktuellen Spieltag
    '''
    if team1_kicktipppunkte > team2_kicktipppunkte:
        team1_punkte = 3
        team2_punkte = 0
    elif team1_kicktipppunkte < team2_kicktipppunkte:
        team1_punkte = 0
        team2_punkte = 3
    else:
        team1_punkte = 1
        team2_punkte = 1
    return (team1_punkte, team2_punkte)


def tordifferenzberechnung_aktueller_spieltag(team1_kicktipppunkte, team2_kicktipppunkte):
    '''
    tordifferenzberechnung berechnet die Tordifferenz des aktuellen Spieltags
    '''
    tordifferenz_mannschaft1 = team1_kicktipppunkte - team2_kicktipppunkte
    tordifferenz_mannschaft2 = team2_kicktipppunkte - team1_kicktipppunkte
    
    return (tordifferenz_mannschaft1, tordifferenz_mannschaft2)

def punkte_tore_tordiff_aktueller_spieltag(spieltag, kicktipp_pfad, jahr)-> List[Tuple[str,int,int,int]]:
    '''
    Punkte, Tore und Tordifferenz für jede Mannschaft für den aktuellen Spieltag zurückgeben (Punkte ergeben sich aus Kicktippunkten, Tore entsprechen den Kicktipppunkten)
    '''
    ergebnis = []
    

    for begegnung in begegnungen_aktueller_spieltag(spieltag, jahr): 

        team1_kicktipppunkte = 0
        mannschaft_1 = ''
        tore_mannschaft1 = 0
        kürzel_coach_1 = ''
        for team1 in vereinsinformationen(spieltag, kicktipp_pfad, jahr):
            if team1.mannschaft == begegnung[0]:
                team1_kicktipppunkte = team1.kicktipppunkte
                mannschaft_1 = team1.mannschaft
                tore_mannschaft1 = team1.kicktipppunkte
                kürzel_coach_1 = team1.kürzel
       
        team2_kicktipppunkte = 0
        mannschaft_2 = ''
        tore_mannschaft2 = 0
        kürzel_coach_2 = ''
        for team2 in vereinsinformationen(spieltag, kicktipp_pfad, jahr):
            if team2.mannschaft == begegnung[1]:
                team2_kicktipppunkte = team2.kicktipppunkte
                mannschaft_2 = team2.mannschaft
                tore_mannschaft2 = team2.kicktipppunkte
                kürzel_coach_2 = team2.kürzel

        punkte_begegnung = punktberechnung_aktueller_spieltag(team1_kicktipppunkte,team2_kicktipppunkte)
        tordifferenz_begegnung = tordifferenzberechnung_aktueller_spieltag(team1_kicktipppunkte, team2_kicktipppunkte)
     
        ergebnis.append((kürzel_coach_1, mannschaft_1, punkte_begegnung[0], tore_mannschaft1, tordifferenz_begegnung[0]))
        ergebnis.append((kürzel_coach_2, mannschaft_2, punkte_begegnung[1], tore_mannschaft2, tordifferenz_begegnung[1]))
            
    return ergebnis



def gesamtpunktberechnung_inkl_vorwoche(spieltag, kicktipp_pfad, jahr, xlsx_path_vorwoche):
    tabelle=pd.DataFrame(punkte_tore_tordiff_aktueller_spieltag(spieltag, kicktipp_pfad, jahr), columns=['Coach', 'Mannschaft','Punkte', 'Tore', 'Tordifferenz'])
    zeilen_der_tabelle=list(tabelle.iterrows())
    liste_für_gesamtpunkte = []
    liste_für_gesamttore = []
    liste_für_gesamttordifferenz = []
    liste_für_vorwochenplatzierung = []
    
    for index, aktuelle_zeile in zeilen_der_tabelle:
        aktuelle_zeile_nur_mannschaft = str(aktuelle_zeile['Mannschaft'])

        vorheriger_spieltag = hilfsfunktionen.excel_to_dataframe(xlsx_path_vorwoche, 'Tabelle')
        debug = False
        if debug:
            print(vorheriger_spieltag)
            print(aktuelle_zeile_nur_mannschaft)
        punkte_für_mannschaft_vorheriger_spieltag = vorheriger_spieltag.loc[vorheriger_spieltag['Mannschaft']== aktuelle_zeile_nur_mannschaft, 'Punkte'].iloc[0]
        tore_für_mannschaft_vorheriger_spieltag = vorheriger_spieltag.loc[vorheriger_spieltag['Mannschaft'] == aktuelle_zeile_nur_mannschaft, 'Tore'].iloc[0]
        tordifferenz_für_mannschaft_vorheriger_spieltag = vorheriger_spieltag.loc[vorheriger_spieltag['Mannschaft'] == aktuelle_zeile_nur_mannschaft, 'Tordifferenz'].iloc[0]
        rang_für_mannschaft_vorheriger_spieltag = vorheriger_spieltag.loc[vorheriger_spieltag['Mannschaft']==aktuelle_zeile_nur_mannschaft, 'Rang'].iloc[0]

        aktuelle_zeile_nur_punkte = int(aktuelle_zeile['Punkte'])
        gesamtpunkte = aktuelle_zeile_nur_punkte + punkte_für_mannschaft_vorheriger_spieltag

        aktuelle_zeile_nur_tore = int(aktuelle_zeile['Tore'])
        gesamttore = aktuelle_zeile_nur_tore + tore_für_mannschaft_vorheriger_spieltag
        
        aktuelle_zeile_nur_tordifferenz = int(aktuelle_zeile['Tordifferenz'])
        gesamttordifferenz = aktuelle_zeile_nur_tordifferenz + tordifferenz_für_mannschaft_vorheriger_spieltag

        vorwochenrang = rang_für_mannschaft_vorheriger_spieltag

        liste_für_gesamtpunkte.append(gesamtpunkte)
        liste_für_gesamttore.append(gesamttore)
        liste_für_gesamttordifferenz.append(gesamttordifferenz)
        liste_für_vorwochenplatzierung.append(vorwochenrang)

    tabelle_mit_gesamtpunkten = tabelle.copy()
    tabelle_mit_gesamtpunkten['Punkte'] = liste_für_gesamtpunkte
    tabelle_mit_gesamtpunkten['Tore'] = liste_für_gesamttore
    tabelle_mit_gesamtpunkten['Tordifferenz']= liste_für_gesamttordifferenz
    tabelle_mit_gesamtpunkten.insert(loc=0, column='Vorwochenplatzierung', value =liste_für_vorwochenplatzierung)

    return tabelle_mit_gesamtpunkten



def rang_berechnung_aktueller_spieltag(tabelle_gesamtpunkte):
    tabelle_sortiert = tabelle_gesamtpunkte.sort_values(by=['Punkte','Tore','Tordifferenz'], ascending=False, ignore_index= True)

    rang_liste = [1]
    previous_row = tabelle_sortiert[['Punkte','Tore','Tordifferenz']].iloc[0]
    rang = 1

    alle_einträge_in_tabelle = list(tabelle_sortiert.iterrows())

    for index, row in alle_einträge_in_tabelle[1::]:
        current_row = row[['Punkte', 'Tore', 'Tordifferenz']]

        if not current_row.equals(previous_row):
            rang = index+1
        
        rang_liste.append(rang)
        previous_row = current_row
    
    tabelle_sortiert.insert(loc=0,column='Rang', value=rang_liste)
    return tabelle_sortiert


def rang_differenzberechnung(spieltag, kicktipp_pfad, jahr, xlsx_path_vorwoche):
    tabelle_gesamtpunkte = gesamtpunktberechnung_inkl_vorwoche(spieltag, kicktipp_pfad, jahr, xlsx_path_vorwoche)
    tabelle_sortiert = rang_berechnung_aktueller_spieltag(tabelle_gesamtpunkte)
    tendenz = tabelle_sortiert['Vorwochenplatzierung'] - tabelle_sortiert['Rang']
    tabelle_mit_vorwochentendenz = tabelle_sortiert.copy()
    tabelle_mit_vorwochentendenz.insert(loc=2, column= 'Tendenz', value =tendenz)
    return tabelle_mit_vorwochentendenz

