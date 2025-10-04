

from db import pripojeni_db, vytvoreni_tabulky, vytvor_databazi
from ukoly import pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol

def hlavni_menu(connection):
    while True:
        print("\n--- Hlavní menu ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        volba = input("Zadejte číslo volby: ").strip()

        if volba == "1":
            pridat_ukol(connection)
        elif volba == "2":
            zobrazit_ukoly(connection)
        elif volba == "3":
            aktualizovat_ukol(connection)
        elif volba == "4":
            odstranit_ukol(connection)
        elif volba == "5":
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

if __name__ == "__main__":
    vytvor_databazi()
    conn = pripojeni_db()
    if conn:
        vytvoreni_tabulky(conn)
        hlavni_menu(conn)
        conn.close()
