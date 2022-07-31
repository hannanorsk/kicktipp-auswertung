import pandas as pd
from spieltagsfunktion import begegnungen_aktueller_spieltag, mannschaft_kicktipppunkte, suche_kürzel_fuer_mannschaft


def begegnungen_kürzel_fuer_kommenden_spieltag(kommender_spieltag, jahr, kicktipp_pfad):

    liste_coaches = []
    for begegnungen in begegnungen_aktueller_spieltag(kommender_spieltag, jahr):
        coach_name_1 = suche_kürzel_fuer_mannschaft(begegnungen[0], kicktipp_pfad=kicktipp_pfad, jahr=jahr)
        coach_name_2 = suche_kürzel_fuer_mannschaft(begegnungen[1], kicktipp_pfad=kicktipp_pfad, jahr=jahr)
        liste_coaches.append((kommender_spieltag, coach_name_1, coach_name_2))

    dataframe_coaches = pd.DataFrame(liste_coaches, columns= ['Spieltag', 'Heimcoach', 'Gastcoach'])

    return dataframe_coaches

def coach_tore_aktueller_spieltag(spieltag, jahr, kicktipp_pfad):
    liste_coaches = []
    for begegnungen in begegnungen_aktueller_spieltag(spieltag, jahr):
        coach_name_1 = suche_kürzel_fuer_mannschaft(begegnungen[0], kicktipp_pfad, jahr)
        coach_name_2 = suche_kürzel_fuer_mannschaft(begegnungen[1], kicktipp_pfad, jahr)
        tore_heim = mannschaft_kicktipppunkte(coach_name_1, spieltag, kicktipp_pfad, jahr)[1]
        tore_gast = mannschaft_kicktipppunkte(coach_name_2, spieltag, kicktipp_pfad, jahr)[1]
        liste_coaches.append((spieltag, coach_name_1, coach_name_2, tore_heim, tore_gast))
    
    dataframe_coach_tore = pd.DataFrame(liste_coaches, columns =['Spieltag', 'Heimcoach', 'Gastcoach', 'Tore Heim', 'Tore Gast'])
    return dataframe_coach_tore

def nächste_begegnungen_kürzel(spieltag, jahr, kicktipp_pfad):
    kommender_spieltag = spieltag +1
    return begegnungen_kürzel_fuer_kommenden_spieltag(kommender_spieltag, jahr, kicktipp_pfad)
        

