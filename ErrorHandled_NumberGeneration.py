import pymysql
import sys


# ===================== CONFIG =====================
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Tiger",
    "database": "Bachpankart",
    "autocommit": False
}

START = 9034000000
END = 9035000000
BATCH_SIZE = 1_00_000


# ===================== MAIN LOGIC =====================
def main():
    connection = None
    cursor = None

    try:
        # ---------- Connect ----------
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("[INFO] Database connected")

        current_start = START
        table_name = "numbers_903x"

        # ---------- Insert Numbers ----------
        batch = []
        total_inserted = 0
        last_num = None
        batch_count = 1

        while current_start < END:
            current_end = min(current_start + BATCH_SIZE, END)

            for number in range(current_start, current_end):
                batch.append((number,))
                total_inserted += 1
                last_num = number

                if len(batch) == BATCH_SIZE:
                    insert_batch(cursor, connection, table_name, batch, batch_count)
                    batch.clear()
                    batch_count += 1

            current_start = current_end

        # ---------- Insert Remaining ----------
        if batch:
            insert_batch(cursor, connection, table_name, batch, batch_count)

        print("\n✅ SUCCESS")
        print(f"Total values inserted: {total_inserted}")
        print(f"Last number inserted: {last_num}")

    except KeyboardInterrupt:
        print("\n[STOPPED] Process interrupted by user")
        if connection:
            connection.rollback()

    except pymysql.MySQLError as e:
        print(f"[DB ERROR] {e}")
        if connection:
            connection.rollback()

    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        if connection:
            connection.rollback()

    finally:
        # ---------- Cleanup ----------
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("[INFO] Database connection closed")


# ===================== HELPERS =====================
def insert_batch(cursor, connection, table_name, batch, batch_no):
    try:
        insert_query = f"INSERT INTO {table_name} (phone) VALUES (%s)"
        print(f"[INFO] Inserting batch {batch_no} ({len(batch)} rows)")
        cursor.executemany(insert_query, batch)
        connection.commit()
    except pymysql.MySQLError as e:
        connection.rollback()
        raise RuntimeError(f"Batch {batch_no} failed: {e}")


# ===================== ENTRY POINT =====================
if __name__ == "__main__":
    main()
