import sqlite3
import time
from datetime import datetime

datoteka_baze = "Baza.sqlite3"


def prodaj_izdelke(seznam_izdelkov, stranka = None, popust = None):
    '''Funkcija dobi dva parametra: seznam izdelkov ter stranko.
       Izda novi račun (tabela Računi) ter s prodanimi izdelki
       dopolni tabelo Prodaje.

       Pokliče funkcijo izbrisi_izdelke(seznam_izdelkov), ki
       v tabeli Izdelki zmanjša količino izdelkov za toliko,
       koliko smo prodali.'''

    c = baza.cursor()
    cas = datetime.now()

    
    # dodamo racun
    c.execute("""INSERT INTO Racuni
                             (datum, kupec) VALUES
                             (?, ?)""", [cas, stranka])
    racun = c.lastrowid

    # slovar: izdelek & kolicina izdelka
    kolicine_izdelkov = {}
    for izdelek in seznam_izdelkov:
        kolicine_izdelkov[izdelek] = kolicine_izdelkov.get(izdelek, 0) + 1

    # dodamo izdelke v tabelo Prodaje
    for izdelek in seznam_izdelkov:
        c.execute("""SELECT cena FROM Izdelki WHERE id = ?""", [izdelek])
        trenutna_cena = c.fetchone()[0]
        
        kolicina = kolicine_izdelkov[izdelek]
        c.execute("""INSERT INTO Prodaje
                            (racun, izdelek, kolicina, trenutna_cena) VALUES
                            (?,?,?,?)""", [racun, izdelek, kolicina, trenutna_cena])
    izbrisi_izdelke(seznam_izdelkov)
    c.close()
    return



# seznam izdelkov = seznam id.jev izdelkov;
# npr.: [2, 2, 5, 6] --> imamo; 2x bela kava, 1x vroča čokolada; 1x vroča čokolada s smetano
def izbrisi_izdelke(seznam_izdelkov):
    '''Funkcija v tabeli Izdelki zmanjša količino izdelkov
       za toliko, kolikor smo jih prodali.'''
    c = baza.cursor()
    
    # slovar: izdelek & kolicina izdelka
    kolicine_izdelkov = {}
    for izdelek in seznam_izdelkov:
        kolicine_izdelkov[izdelek] = kolicine_izdelkov.get(izdelek, 0) + 1

    # izbrišemo oz. ''osvežimo tabelo Izdelki''
    for izdelek in kolicine_izdelkov:
        kolicina = kolicine_izdelkov[izdelek]

        c.execute("""SELECT trenutna_kolicina FROM Izdelki WHERE id = ?""", [izdelek])
        kol = c.fetchone()[0]
        
        c.execute("""UPDATE Izdelki
                            SET trenutna_kolicina = ?
                            WHERE id = ?""", [kol-kolicina, izdelek])
    c.close()
    return


    
def dodaj_stranko(stranka, davcna):
    '''Če stranka še ni v bazi, jo funkcija doda
       (razen, če želi stranka ostati anonimna).'''
    c = baza.cursor()
    c.execute("""SELECT ime FROM Kupci WHERE ime = ?""", [stranka])
    s = c.fetchone()
    if s is None:
        c.execute("""INSERT INTO Kupci
                                 (ime, davcna) VALUES
                                 (?, ?)""", [stranka, davcna])
        stranka = c.lastrowid
    c.close()
    return



def dodaj_narocilo(ID, kol):
    '''Funkcija spremeni tabelo Naročila tako, da zapiše
       katere izdelke smo naročili ter koliko katerega.'''
    c = baza.cursor()
    
    # narocilo
    c.execute("""SELECT id FROM Izdelki WHERE id = ?""", [ID])
    id_izd = c.fetchone()[0]
    
    c.execute("""INSERT INTO Narocila
                             (izdelek, dodatna_kolicina) VALUES
                             (?, ?)""", [id_izd, kol])

    # povečanje trenutne količine izdelka
    c.execute("""SELECT trenutna_kolicina FROM Izdelki WHERE id = ?""", [ID])
    tre_kol = c.fetchone()[0]    
    c.execute("""UPDATE Izdelki
                            SET trenutna_kolicina = ?
                            WHERE id = ?""", [tre_kol+kol, ID])    

    c.close()
    return











#priklopimo se na bazo
baza = sqlite3.connect(datoteka_baze, isolation_level=None)
