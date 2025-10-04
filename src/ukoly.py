import mysql.connector

def ziskat_vstup(vstup):
    """Funkce pro získání neprázdného vstupu od uživatele."""
    while True:
        try:
            hodnota = input(vstup).strip()
            if not hodnota:
                print("Chyba: Tento údaj nesmí být prázdný!")
                continue
            return hodnota
        except KeyboardInterrupt:
            print("\nOperace přerušena uživatelem.")
            return None
        except Exception as e:
            print(f"Něco se nepovedlo: {e}")
            return None

def pridat_ukol(connection):
    nazev = ziskat_vstup("Zadejte název úkolu: ")
    popis = ziskat_vstup("Zadejte popis úkolu: ")

    if nazev is None or popis is None:
        return

    pridat_ukol_db(connection, nazev, popis)

def pridat_ukol_db(connection, nazev, popis):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ukoly (nazev, popis, stav)
                VALUES (%s, %s, %s)
                """,
                (nazev, popis, "nezahájeno"),
            )
        connection.commit()
        print("Úkol byl přidán.")
    except mysql.connector.Error as e:
        connection.rollback()
        raise Exception(f"Chyba při přidávání úkolu: {e}")

def zobrazit_ukoly(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nazev, popis, stav, datum_vytvoreni
                FROM ukoly
                WHERE stav IN ('nezahájeno', 'probíhá', 'hotovo')
                """
            )
            vysledky = cursor.fetchall()
            if not vysledky:
                print("Žádné úkoly.")
                return
            
            print("\n{:<5} {:<20} {:<30} {:<12} {:<19}".format("ID", "Název", "Popis", "Stav", "Vytvořeno"))
            print("-" * 90)

            # Výpis každého řádku
            for u in vysledky:
                print("{:<5} {:<20} {:<30} {:<12} {:<19}".format(
                    u[0],
                    (u[1][:20] + "...") if len(u[1]) > 20 else u[1],
                    (u[2][:30] + "...") if len(u[2]) > 30 else u[2],
                    u[3],
                    str(u[4])[:19]
                ))
            
    except:
        print("Chyba při načítání.")

def aktualizovat_ukol(connection):
    zobrazit_ukoly(connection)
    id_vstup = input("Zadejte ID úkolu, který chcete aktualizovat: ").strip()

    if not id_vstup:
        print("Chyba: Musíte zadat ID úkolu.")
        return

    try:
        id_ukolu = int(id_vstup)
    except ValueError:
        print("Chyba: Zadejte platné číselné ID.")
        return

    if not overit_existenci_ukolu(connection, id_ukolu):
        print(f"Úkol s ID {id_ukolu} neexistuje.")
        return

    novy_stav = input("Zadejte nový stav (probíhá/hotovo): ").strip().lower()
    if novy_stav not in ["probíhá", "hotovo"]:
        print("Neplatný stav. Povolené hodnoty jsou 'probíhá' nebo 'hotovo'.")
        return

    try:
        aktualizovat_ukol_db(connection, id_ukolu, novy_stav)
        print("\nÚkol byl úspěšně aktualizován.")
    except Exception as e:
        print(f"Nastala neočekávaná chyba při aktualizaci: {e}")

def aktualizovat_ukol_db(connection, id_ukolu, novy_stav):
    try:
        with connection.cursor() as cursor:
            dotaz = "UPDATE ukoly SET stav = %s WHERE id = %s"
            cursor.execute(dotaz, (novy_stav, id_ukolu))
        connection.commit()
    except Exception as e:
        print(f"Chyba při aktualizaci úkolu: {e}")
        connection.rollback()

def overit_existenci_ukolu(connection, id_ukolu):
    try:
        with connection.cursor() as cursor:
            dotaz = "SELECT COUNT(*) FROM ukoly WHERE id = %s"
            cursor.execute(dotaz, (id_ukolu,))
            (pocet,) = cursor.fetchone()
            return pocet > 0
    except Exception as e:
        print(f"Chyba při ověřování existence úkolu: {e}")
        return False

def odstranit_ukol(connection):
    zobrazit_ukoly(connection)
    id_vstup = input("Zadejte ID úkolu, který chcete odstranit: ").strip()

    if not id_vstup:
        print("Chyba: Musíte zadat ID úkolu.")
        return

    try:
        id_ukolu = int(id_vstup)
    except ValueError:
        print("Chyba: Zadejte platné číselné ID.")
        return

    if not overit_existenci_ukolu(connection, id_ukolu):
        print(f"Úkol s ID {id_ukolu} neexistuje.")
        return

    try:
        odstranit_ukol_db(connection, id_ukolu)
        print("\nÚkol byl úspěšně odstraněn.")
    except Exception as e:
        print(f"Nastala neočekávaná chyba při odstraňování: {e}")

def odstranit_ukol_db(connection, id_ukolu):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
        connection.commit()
    except:
        connection.rollback()
