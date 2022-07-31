from os import error, path

from pandas.core.frame import DataFrame
from pandas.io import excel
import nächste_begegnungen
from pandas import ExcelWriter
import spieltagsfunktion
import pandas as pd
import os
import constants


def path_auswertungsdatei(kicktipp_ordner, jahr, spieltag):
        dateiname = 'Tabelle_Begegnungen'+str(spieltag)+'.xlsx'
        xlsx_path = os.path.join(kicktipp_ordner, constants.unterordner_output, str(jahr), dateiname)
        return xlsx_path

def erstelle_auswertungsdatei_spieltag_1(jahr, kicktipp_ordner):
    
    tabelle_gesamtpunkte =pd.DataFrame(spieltagsfunktion.punkte_tore_tordiff_aktueller_spieltag(1, kicktipp_ordner, jahr), columns=['Coach', 'Mannschaft','Punkte', 'Tore', 'Tordifferenz'])
    tabelle = spieltagsfunktion.rang_berechnung_aktueller_spieltag(tabelle_gesamtpunkte)
    excel_pfad_auswertungsdatei= erstelle_auswertungsdatei(spieltag=1, jahr=jahr, tabelle=tabelle, kicktipp_ordner=kicktipp_ordner)
    return excel_pfad_auswertungsdatei

def erstelle_auswertungsdatei_ab_spieltag_2(spieltag, jahr, xlsx_path_vorwoche, kicktipp_pfad):
    
    tabelle = spieltagsfunktion.rang_differenzberechnung(spieltag, kicktipp_pfad, jahr, xlsx_path_vorwoche)
    excel_pfad_auswertungsdatei = erstelle_auswertungsdatei(spieltag, jahr, tabelle, kicktipp_pfad) 
    return excel_pfad_auswertungsdatei
            
def erstelle_auswertungsdatei(spieltag: int, jahr: int, tabelle: DataFrame, kicktipp_ordner):
    excel_pfad_auswertungsdatei = path_auswertungsdatei(kicktipp_ordner, jahr, spieltag) 
   
        
    with ExcelWriter(excel_pfad_auswertungsdatei) as writer:
        nächste_begegnungen.coach_tore_aktueller_spieltag(spieltag, jahr, kicktipp_ordner).to_excel(writer, 'Ergebnisse aktueller Spieltag', index = False)
        
        tabelle.to_excel(writer, 'Tabelle', index=False)
        nächste_begegnungen.nächste_begegnungen_kürzel(spieltag, jahr, kicktipp_ordner).to_excel(writer, 'nächste Begegnungen', index=False)
        writer.save()
    return excel_pfad_auswertungsdatei