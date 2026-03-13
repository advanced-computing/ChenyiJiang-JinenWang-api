import duckdb


def update_database():
    conn = duckdb.connect("cpi.db")
    file_2025 = "PCPI25M2.csv"

    print(f"Updating database with {file_2025}...")

    # ==========================================
    # 1. Append
    # ==========================================

    conn.sql(
        f"INSERT INTO cpi_append SELECT * FROM read_csv('{file_2025}', auto_detect=true)"
    )
    print("✅ Applied Append logic.")

    # ==========================================
    # 2. Truncate
    # ==========================================

    conn.sql("DELETE FROM cpi_trunc")
    conn.sql(
        f"INSERT INTO cpi_trunc SELECT * FROM read_csv('{file_2025}', auto_detect=true)"
    )
    print("✅ Applied Truncate logic.")

    # ==========================================
    # 3. Incremental
    # ==========================================

    conn.sql(f"""
        DELETE FROM cpi_inc 
        WHERE DATE IN (SELECT DATE FROM read_csv('{file_2025}', auto_detect=true))
    """)
    conn.sql(
        f"INSERT INTO cpi_inc SELECT * FROM read_csv('{file_2025}', auto_detect=true)"
    )
    print("✅ Applied Incremental logic.")

    print("\n--- Final Row Counts ---")
    print("cpi_append rows:", conn.sql("SELECT COUNT(*) FROM cpi_append").fetchone()[0])
    print("cpi_trunc rows: ", conn.sql("SELECT COUNT(*) FROM cpi_trunc").fetchone()[0])
    print("cpi_inc rows:   ", conn.sql("SELECT COUNT(*) FROM cpi_inc").fetchone()[0])

    conn.close()


if __name__ == "__main__":
    update_database()
