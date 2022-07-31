import os


def eingabe_ordner_anlegen(kicktipp_pfad, eingabe_ordner, jahr):
    '''
    Prüft, ob der Hauptordner "Kicktipp" existiert, wenn nicht wird angezeigt, dass dieser angelegt werden soll oder in der config_datei ein existierender Ordner eingegeben werden soll.
    Danach wird geprüft, ob die Ordnerstruktur für die Eingabedateien bereits existiert. Wenn nicht, werden die entsprechenden Ordner angelegt, sodass die CSV-Export-Dateien dort abgespeichert werden können.
    '''

    if not os.path.exists(kicktipp_pfad):
        raise FileNotFoundError("Der Kicktipp-Ordner "+kicktipp_pfad+" existiert nicht. Bitte den Ordner anlegen oder in der config_datei einen einstellen, der existiert.")
   
    ordner_pfad_zu_csv_dateien = os.path.join(kicktipp_pfad, eingabe_ordner, str(jahr))
    if not os.path.exists(ordner_pfad_zu_csv_dateien):
        os.makedirs(ordner_pfad_zu_csv_dateien)


def ausgabe_ordner_anlegen(kicktipp_pfad, ausgabe_ordner, jahr):
    '''
    Prüft, ob der Hauptordner "Kicktipp" existiert, wenn nicht wird angezeigt, dass dieser angelegt werden soll oder in der config_datei ein existierender Ordner eingegeben werden soll.
    Danach wird geprüft, ob die Ordnerstruktur für die Auswertungsdateien bereits existiert. Wenn nicht, werden die entsprechenden Ordner angelegt, sodass die Auswertungs-Dateien dort abgespeichert werden können.
    '''
    if not os.path.exists(kicktipp_pfad):
        raise FileNotFoundError("Der Kicktipp-Ordner "+kicktipp_pfad+" existiert nicht. Bitte den Ordner anlegen oder in der config_datei einen einstellen, der existiert.")
    
    ordner_pfad_zu_auswertungsdatei = os.path.join(kicktipp_pfad, ausgabe_ordner, str(jahr)) 
    if not os.path.exists(ordner_pfad_zu_auswertungsdatei):
        os.makedirs(ordner_pfad_zu_auswertungsdatei)