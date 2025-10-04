import mysql.connector

def vytvor_databazi():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2354"  # nebo task_user, podle toho co používáš
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_manager")
        print("Databáze vytvořena nebo už existuje.")
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Chyba při vytváření databáze: {e}")

def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2354",
            database="task_manager"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Chyba připojení: {e}")
        return None

def vytvoreni_tabulky(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ukoly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR(255) NOT NULL,
                    popis TEXT NOT NULL,
                    stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
                    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Chyba při vytváření tabulky: {e}")
