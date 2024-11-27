import sqlite3

def inspect_database(db_path):
    """
    Inspect the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables:", cursor.fetchall())

    # Inspecionar a tabela guest_checks
    cursor.execute("SELECT * FROM guest_checks LIMIT 5;")
    print("Guest Checks Sample:", cursor.fetchall())

    conn.close()

if __name__ == "__main__":
    db_path = "cb_lab_dados.sqlite"
    inspect_database(db_path)
