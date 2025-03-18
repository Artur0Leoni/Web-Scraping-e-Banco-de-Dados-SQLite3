import sqlite3


def create_database():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            title TEXT,
            price REAL,
            price_pix REAL,
            installment_value REAL,
            installment_count INTEGER,
            technical_info TEXT,
            updated_at TEXT
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()