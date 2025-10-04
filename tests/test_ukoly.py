import pytest
from src.db import pripojeni_db
from src.ukoly import pridat_ukol_db, aktualizovat_ukol_db, odstranit_ukol_db

@pytest.fixture(scope="module")
def connection():
    conn = pripojeni_db()
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def cleanup_db(connection):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM ukoly")
    connection.commit()
    yield
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM ukoly")
    connection.commit()

def test_pridat_ukol_pozitivni(connection):
    nazev, popis = "Test Úkol", "Popis úkolu"
    pridat_ukol_db(connection, nazev, popis)
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ukoly WHERE nazev=%s AND popis=%s", (nazev, popis))
        (count,) = cursor.fetchone()
    assert count == 1

def test_pridat_ukol_negativni(connection):
    nazev, popis = "", "Popis"
    with pytest.raises(Exception):
        pridat_ukol_db(connection, nazev, popis)

def test_aktualizovat_ukol_pozitivni(connection):
    pridat_ukol_db(connection, "Aktualizuj", "Test aktualizace")
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev=%s", ("Aktualizuj",))
        (ukol_id,) = cursor.fetchone()
    aktualizovat_ukol_db(connection, ukol_id, "hotovo")
    with connection.cursor() as cursor:
        cursor.execute("SELECT stav FROM ukoly WHERE id=%s", (ukol_id,))
        (stav,) = cursor.fetchone()
    assert stav == "hotovo"

def test_aktualizovat_ukol_negativni(connection):
    with pytest.raises(Exception):
        aktualizovat_ukol_db(connection, 9999999, "hotovo")

def test_odstranit_ukol_pozitivni(connection):
    pridat_ukol_db(connection, "Smazat", "Úkol na smazání")
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev=%s", ("Smazat",))
        (ukol_id,) = cursor.fetchone()
    odstranit_ukol_db(connection, ukol_id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ukoly WHERE id=%s", (ukol_id,))
        (count,) = cursor.fetchone()
    assert count == 0

def test_odstranit_ukol_negativni(connection):
    with pytest.raises(Exception):
        odstranit_ukol_db(connection, 9999999)
