import csv
import sqlite3


def lue_csv_tietokantaan(tiedostonimi: str, ei_huomioon: list, lokaatiot: list):
    """
    Luetaan csv:stä sisältö ja luodaan tietokanta ja taulut\n
    Parametrit:
    - tiedostonimi, luettavan tiedoston nimi
    - ei_huomioon, solujen tieto, mikä halutaan hyppää yli
    - lokaatiot: Mahdollinen lokaatio, jos hahmot halutaan sitoa sellaiseen
    Metodit:
    - luo_tietokanta_ja_taulut()
    - lisaa_tietokantaan()
    Huomiona:
    - Huomioi encoding parametri, luettavan tiedoston mukaan: https://docs.python.org/3/library/codecs.html
    - Tietokannan nimi on tässä oletettu, parametria ei siis tarjota
    """
    try:
        with open(tiedostonimi) as tiedosto:
            lokaatio = ""    
            for rivi in csv.reader(tiedosto, delimiter=";"):
                if rivi[0] in ei_huomioon:
                    continue
                if rivi[0] in lokaatiot:
                    lokaatio = rivi[0].replace(" ", "_") # Vaihdetaan välit alaviivaan
                    luo_tietokanta_ja_taulu(lokaatio)
                if rivi[0] not in lokaatiot:
                    lisaa_tietokantaan(rivi[0:13], lokaatio) # Ylimääräisiä soluja ei oteta huomioon                     
    except:
        print("Tiedoston lukeminen epäonnistui")
          


def luo_yhteys_tietokantaan(tietokannan_nimi="NPC.db"):
    """
    Luodaan tietokantaan yhteys ja palautetaan yhteys-objekti
    """
    try:
        db = sqlite3.connect(tietokannan_nimi)
        db.isolation_level = None 
        return db
    except:
        print("Yhteyden luominen tietokantaan epäonnistui")    

def luo_tietokanta_ja_taulu(taulun_nimi: str, tietokannan_nimi="NPC.db"):
    """
    Luodaan tietokanta ja lisätään taulut
    - Oletusnimi tietokannalle on NPC.db
    - Tauluja ei luoda, jos ne on olemassa
    """
    try:
        db = luo_yhteys_tietokantaan(tietokannan_nimi)
        sql = f"""CREATE TABLE IF NOT EXISTS {taulun_nimi} (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL UNIQUE, level INTEGER, hits INTEGER, at INTEGER, 
                db INTEGER, shield TEXT, greaves TEXT, mel_ob INTEGER, msle_ob INTEGER, 
                mov_m INTEGER , class TEXT, race TEXT, notes TEXT)"""
        db.execute(sql) # Injektiot estetty?
    except:
        print(f"Taulun luominen epäonnistui: {taulun_nimi}")        


def lisaa_tietokantaan(lisattavat_tiedot: list, taulun_nimi: str, tietokannan_nimi="NPC.db"):
    """
    Parametrit
    - lisattavat_tiedot: lisättävä tieto listana
    - taulun_nimi: taulu tietokannassa, mihin lisätään
    - tietokannan_nimi: lisättävä tietokanta(polku), oletuksena NPC.db
    """
    db = luo_yhteys_tietokantaan(tietokannan_nimi)
    sql = f"""INSERT INTO {taulun_nimi} (
        name, level, hits, at, db, shield, 
        greaves, mel_ob, msle_ob, mov_m, class, race, notes) 
        VALUES (?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    try:    
        db.execute(sql, lisattavat_tiedot) # Injektio estetty   
    except:
        print(f"Tauluun {taulun_nimi} lisääminen epäonnistui.")

if __name__ == "__main__":
    ei_huomioon = ["IN THARBAD", "Name"]
    lokaatiot = [ # Lokaatiot toimii taulun nimenä tietokannassa
                "Pohjoisranta", "Etelaranta", "Satama", 
                "Varkaiden kaupunki", "Kuninkaan Katu", 
                "Rahvaan kaupunginosa", "Kauppiaiden kaupunginosa",
                "Sekalaisia", "Kiristajaliiga", "Rosvot",
                "Maantierosvot 1410", "Maantierosvot 1640"]
    lue_csv_tietokantaan("raakadata.csv", ei_huomioon, lokaatiot)
    
