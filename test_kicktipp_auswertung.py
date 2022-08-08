import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import auswertung
import spieltagsfunktion
import os
import hilfsfunktionen
import constants
import datei_ordner_pfade


kicktipp_pfad = 'test'        
jahr =2021
ausgabe_ordner = constants.unterordner_output



class TestKicktippAuswertung(unittest.TestCase):
    def setUpClass():
        datei_ordner_pfade.ausgabe_ordner_anlegen(kicktipp_pfad, constants.unterordner_output, jahr)


    def tearDownClass():
        os.remove(TestKicktippAuswertung.pfad_ausgegebenes_Excel(1, 2021))
        os.remove(TestKicktippAuswertung.pfad_ausgegebenes_Excel(2, 2021))
        os.rmdir(hilfsfunktionen.ordner_pfad_auswertungsdatei(kicktipp_pfad, ausgabe_ordner, jahr))
    

    def test_kicktipp_auswertung_excel1(self):
        '''
        Diese Funktion testet, ob die Auswertung für den ersten Spieltag stimmt.
        '''
        spieltag = 1

        auswertung.erstelle_auswertungsdatei_spieltag_1(jahr=jahr, kicktipp_ordner=kicktipp_pfad)
        erwartetes_Ergebnis = self.erwartetes_Ergebnis_Sheet(spieltag, 'Tabelle')
        ausgegebene_Excel = self.ausgegebenes_Excel_Sheet(spieltag, 'Tabelle', jahr)
                
        assert_frame_equal(ausgegebene_Excel, erwartetes_Ergebnis)
        
     
    def test_kicktipp_auswertung_excel2(self):
        '''
        Diese Funktion testet, ob die Auswertung für den zweiten Spieltag stimmt.
        '''
        spieltag = 2
        xlsx_path_vorwoche = os.path.join('test', 'erwartetes_Ergebnis', 'Kicktipp_Auswertung_Spieltag1.xlsx')

        auswertung.erstelle_auswertungsdatei_ab_spieltag_2(spieltag, jahr=jahr, xlsx_path_vorwoche=xlsx_path_vorwoche, kicktipp_pfad=kicktipp_pfad)
        # Vergleiche Sheet 'Tabelle'
        erwartetes_Ergebnis = self.erwartetes_Ergebnis_Sheet(spieltag, 'Tabelle')
        ausgegebene_Excel = self.ausgegebenes_Excel_Sheet(spieltag, 'Tabelle', jahr)
        assert_frame_equal(ausgegebene_Excel, erwartetes_Ergebnis)

        # Vergleiche Sheet 'Ergebnisse aktueller Spieltag'
        erwartetes_Ergebnis = self.erwartetes_Ergebnis_Sheet(spieltag, 'Ergebnisse aktueller Spieltag').sort_values('Heimcoach', ignore_index = True)
        ausgegebene_Excel = self.ausgegebenes_Excel_Sheet(spieltag, 'Ergebnisse aktueller Spieltag', jahr).sort_values('Heimcoach', ignore_index = True)
        assert_frame_equal(ausgegebene_Excel, erwartetes_Ergebnis)

        # Vergleiche Sheet 'nächste Begegnungen'
        erwartetes_Ergebnis = self.erwartetes_Ergebnis_Sheet(spieltag, 'nächste Begegnungen').sort_values('Heimcoach', ignore_index = True)
        ausgegebene_Excel = self.ausgegebenes_Excel_Sheet(spieltag, 'nächste Begegnungen', jahr).sort_values('Heimcoach', ignore_index = True)
        assert_frame_equal(ausgegebene_Excel, erwartetes_Ergebnis)
        

    def erwartetes_Ergebnis_Sheet(self, spieltag, sheet_name):
        kicktipp_pfad = os.path.join('test','erwartetes_Ergebnis')
        return pd.read_excel(io= os.path.join(kicktipp_pfad,'Kicktipp_Auswertung_Spieltag'+str(spieltag)+'.xlsx'), sheet_name=sheet_name)

    def ausgegebenes_Excel_Sheet(self, spieltag, sheet_Name, jahr):
        return pd.read_excel(io=TestKicktippAuswertung.pfad_ausgegebenes_Excel(spieltag, jahr), sheet_name=sheet_Name)

    def pfad_ausgegebenes_Excel(spieltag, jahr):

        return auswertung.path_auswertungsdatei(kicktipp_pfad, jahr=jahr, spieltag=spieltag)

    def test_punktberechnung(self):
        team1_kicktipppunkte = 18
        team2_kicktipppunkte = 15
        team_punkte = spieltagsfunktion.punktberechnung_aktueller_spieltag(team1_kicktipppunkte,team2_kicktipppunkte)
        self.assertEqual(team_punkte[0], 3, 'Punkte für Team 1 stimmen nicht')
        self.assertEqual(team_punkte[1], 0, 'Punkte für Team 2 stimmen nicht')
        
        team1_kicktipppunkte2 = 15
        team2_kicktipppunkte2 = 18
        team_punkte2 = spieltagsfunktion.punktberechnung_aktueller_spieltag(team1_kicktipppunkte2, team2_kicktipppunkte2)
        self.assertEqual(team_punkte2[0], 0, 'Punkte für Team 1 stimmen nicht')
        self.assertEqual(team_punkte2[1], 3, 'Punkte für Team 2 stimmen nicht')

        team1_kicktipppunkte3 = 15
        team2_kicktipppunkte3 = 15
        team_punkte3 = spieltagsfunktion.punktberechnung_aktueller_spieltag(team1_kicktipppunkte3,team2_kicktipppunkte3)
        self.assertEqual(team_punkte3[0], 1)
        self.assertEqual(team_punkte3[1], 1)


if __name__ == '__main__':
    unittest.main()